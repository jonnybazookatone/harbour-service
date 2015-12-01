"""
Test webservices
"""
import mock
import testing.postgresql

from flask.ext.testing import TestCase
from flask import url_for
from classic import app
from classic.models import db, Users
from classic.http_errors import CLASSIC_AUTH_FAILED, CLASSIC_DATA_MALFORMED, CLASSIC_TIMEOUT, CLASSIC_BAD_MIRROR,\
    CLASSIC_NO_COOKIE, CLASSIC_UNKNOWN_ERROR, MYADS_TIMEOUT, MYADS_UNKNOWN_ERROR, NO_CLASSIC_ACCOUNT
from stub_response import ads_classic_200, ads_classic_unknown_user, ads_classic_wrong_password, ads_classic_no_cookie,\
    ads_classic_fail, myads_200, myads_fail, ads_classic_libraries_200
from httmock import HTTMock
from requests.exceptions import Timeout


USER_ID_KEYWORD = 'X-Adsws-Uid'


class TestEndpoints(TestCase):
    """
    Tests http endpoints
    """

    def create_app(self):
        """
        Create the wsgi application
        """
        app_ = app.create_app()
        app_.config['CLASSIC_LOGGING'] = {}
        app_.config['ADS_CLASSIC_MIRROR_LIST'] = ['mirror.com']
        app_.config['CLASSIC_MYADS_USER_DATA_URL'] = 'http://myads.net'
        return app_

    def setUp(self):
        self.stub_user_data = {
            'classic_email': 'user@ads.com',
            'classic_password': 'password',
            'classic_mirror': 'mirror.com'
        }

    def test_user_authentication_success(self):
        """
        Tests the end point of a user authenticating their ADS credentials via the web app
        """
        # 1. The user fills in their credentials
        # 2. The user submits their credentials to the end point
        url = url_for('AuthenticateUser'.lower())

        with HTTMock(ads_classic_200) as ads, HTTMock(myads_200) as myads:
            r = self.client.post(url, data=self.stub_user_data)

        self.assertStatus(r, 200)

        self.assertEqual(
            r.json['classic_email'],
            self.stub_user_data['classic_email']
        )
        self.assertTrue(r.json['classic_authed'])

    def test_user_authentication_unknown_user(self):
        """
        Tests the end point of a user authenticating their ADS credentials via the web app
        """
        url = url_for('AuthenticateUser'.lower())

        with HTTMock(ads_classic_unknown_user):
            r = self.client.post(url, data=self.stub_user_data)

        self.assertStatus(r, CLASSIC_AUTH_FAILED['code'])
        self.assertEqual(r.json['error'], CLASSIC_AUTH_FAILED['message'])

    def test_user_authentication_wrong_password(self):
        """
        Tests the end point of a user authenticating their ADS credentials via the web app
        """
        url = url_for('AuthenticateUser'.lower())

        with HTTMock(ads_classic_wrong_password):
            r = self.client.post(url, data=self.stub_user_data)

        self.assertStatus(r, CLASSIC_AUTH_FAILED['code'])
        self.assertEqual(r.json['error'], CLASSIC_AUTH_FAILED['message'])

    @mock.patch('classic.views.requests.post')
    def test_ads_classic_timeout(self, mocked_post):
        """
        Test that the service catches timeouts and returns a HTTP error response
        """
        mocked_post.side_effect = Timeout

        url = url_for('AuthenticateUser'.lower())
        r = self.client.post(url, data=self.stub_user_data)

        self.assertStatus(r, CLASSIC_TIMEOUT['code'])
        self.assertEqual(r.json['error'], CLASSIC_TIMEOUT['message'])

    def test_missing_data_given_fails(self):
        """
        Pass data that is missing content that is needed
        """
        url = url_for('AuthenticateUser'.lower())

        data1 = {'classic_email': 'email'}
        data2 = {'classic_password': 'password'}
        data3 = {'classic_mirror': 'mirror'}
        data4 = {'classic_password': 'password', 'classic_mirror': 'mirror'}
        data5 = {'classic_email': 'email', 'classic_password': 'password'}
        data6 = {'cassic_email': 'email', 'clasic_mirror': 'mirror'}
        data7 = {}
        data_list = [data1, data2, data3, data4, data5, data6, data7]

        for data in data_list:
            r = self.client.post(url, data=data)
            self.assertStatus(r, CLASSIC_DATA_MALFORMED['code'])
            self.assertEqual(r.json['error'], CLASSIC_DATA_MALFORMED['message'])

    def test_mismatching_emails_on_auth(self):
        """
        Just a sanity check that if the e-mail sent, and the e-mail returned after authentification, match one another
        """
        # 1. The user fills in their credentials
        user_data = self.stub_user_data.copy()
        user_data['classic_email'] = 'different@email.com'

        # 2. The user submits their credentials to the end point
        url = url_for('AuthenticateUser'.lower())

        with HTTMock(ads_classic_200):
            r = self.client.post(url, data=user_data)

        self.assertStatus(r, CLASSIC_AUTH_FAILED['code'])
        self.assertEqual(r.json['error'], CLASSIC_AUTH_FAILED['message'])

    def test_incorrect_mirror_given(self):
        """
        Tests that an HTTP error is given if the mirror site is not known
        """
        # 1. The user fills in their credentials
        user_data = self.stub_user_data.copy()
        user_data['classic_mirror'] = 'nonexistentmirror'

        # 2. The user submits their credentials to the end point
        url = url_for('authenticateuser')
        r = self.client.post(url, data=user_data)

        self.assertStatus(r, CLASSIC_BAD_MIRROR['code'])
        self.assertEqual(r.json['error'], CLASSIC_BAD_MIRROR['message'])

    def test_classic_does_not_return_cookie(self):
        """
        In the (unlikely) scenario that ADS Classic does not return a cookie for the user, we need to handle that
        """
        url = url_for('authenticateuser')
        with HTTMock(ads_classic_no_cookie):
            r = self.client.post(url, data=self.stub_user_data)
        self.assertStatus(r, CLASSIC_NO_COOKIE['code'])
        self.assertEqual(r.json['error'], CLASSIC_NO_COOKIE['message'])

    def test_ads_classic_any_non_unknown_response(self):
        """
        Test that the error message for an unknown error from myADS is returned. When we know the exact errors, this
        message can be updated to be more specific
        """
        url = url_for('authenticateuser')

        with HTTMock(ads_classic_fail) as ads:
            r = self.client.post(url, data=self.stub_user_data)

        self.assertStatus(r, CLASSIC_UNKNOWN_ERROR['code'])
        self.assertIn(CLASSIC_UNKNOWN_ERROR['message'], r.json['error'])

        self.assertIn('ads_classic', r.json)
        self.assertIn('message', r.json['ads_classic'])
        self.assertIn('status_code', r.json['ads_classic'])

    @mock.patch('classic.views.client')
    def test_myads_timesout(self, mocked_client):
        """
        In the scenario myADS times out before responding, we need to inform the user
        """
        client_instance = mocked_client.return_value
        client_instance.post.side_effect = Timeout

        url = url_for('authenticateuser')

        with HTTMock(ads_classic_200):
            r = self.client.post(url, data=self.stub_user_data)

        self.assertStatus(r, MYADS_TIMEOUT['code'])
        self.assertEqual(r.json['error'], MYADS_TIMEOUT['message'])

    def test_myads_any_non_200_fail_response(self):
        """
        Test that the error message for an unknown error from myADS is returned. When we know the exact errors, this
        message can be updated to be more specific
        """
        url = url_for('authenticateuser')

        with HTTMock(ads_classic_200) as ads, HTTMock(myads_fail) as myads:
            r = self.client.post(url, data=self.stub_user_data)

        self.assertStatus(r, MYADS_UNKNOWN_ERROR['code'])
        self.assertIn(MYADS_UNKNOWN_ERROR['message'], r.json['error'])

        self.assertIn('myads', r.json)
        self.assertIn('message', r.json['myads'])
        self.assertIn('status_code', r.json['myads'])


class TestClassicLibrariesEndpoint(TestCase):
    """
    Test class for GET end point to acquire libraries
    """
    postgresql_url_dict = {
        'port': 1234,
        'host': '127.0.0.1',
        'user': 'postgres',
        'database': 'test'
    }
    postgresql_url = 'postgresql://{user}@{host}:{port}/{database}'\
        .format(
            user=postgresql_url_dict['user'],
            host=postgresql_url_dict['host'],
            port=postgresql_url_dict['port'],
            database=postgresql_url_dict['database']
        )

    def create_app(self):
        """
        Create the wsgi application
        """
        app_ = app.create_app()
        app_.config['CLASSIC_LOGGING'] = {}
        app_.config['SQLALCHEMY_BINDS'] = {}
        app_.config['ADS_CLASSIC_MIRROR_LIST'] = ['mirror.com']
        app_.config['SQLALCHEMY_BINDS']['imports'] = TestClassicLibrariesEndpoint.postgresql_url

        return app_

    @classmethod
    def setUpClass(cls):
        cls.postgresql = \
            testing.postgresql.Postgresql(**cls.postgresql_url_dict)

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()

    def setUp(self):
        """
        Set up the database for use
        """
        db.create_all()

    def tearDown(self):
        """
        Remove/delete the database and the relevant connections
        """
        db.session.remove()
        db.drop_all()

    @mock.patch('classic.views.request')
    def test_get_libraries_end_point(self, mocked_request):
        """
        Test the workflow of successfully retrieving a set of classic libraries
        """
        stub_get_libraries = {
            'libraries': [
                {
                    'name': 'Name',
                    'description': 'Description',
                    'documents': [
                        '2015MNRAS.446.4239E', '2015A&C....10...61E', '2014A&A...562A.100E', '2013A&A...556A..23E'
                    ]
                }
            ]
        }

        # 1. The user is identified via header information
        # - Generate dummy user in database
        # - Give the header the correct information
        headers = {USER_ID_KEYWORD: 10}
        mocked_request.headers = headers
        user = Users(absolute_uid=10, classic_cookie='ef9df8ds', classic_mirror='mirror.com')
        db.session.add(user)
        db.session.commit()

        # 2. The database is checked to see if the user exists, and the cookie retrieved
        # 3. The ADS Classic end point is contacted, returning a 200, and the content returned
        url = url_for('classiclibraries')
        with HTTMock(ads_classic_libraries_200):
            r = self.client.get(url)
        self.assertStatus(r, 200)
        self.assertEqual(r.json['libraries'], stub_get_libraries['libraries'])

    @mock.patch('classic.views.request')
    def test_get_libraries_when_the_user_does_not_exist(self, mocked_request):
        """
        Test that when a user does not exist within the database, that the libraries end point returns a known error
        message
        """
        headers = {USER_ID_KEYWORD: 10}
        mocked_request.headers = headers

        url = url_for('classiclibraries')
        r = self.client.get(url)

        self.assertStatus(r, NO_CLASSIC_ACCOUNT['code'])
        self.assertEqual(r.json['error'], NO_CLASSIC_ACCOUNT['message'])

    @mock.patch('classic.views.request')
    @mock.patch('classic.views.requests.get')
    def test_get_libraries_when_ads_classic_timesout(self, mocked_get, mocked_request):
        """
        Test that if ADS Classic times out before finishing the request, that the libraries end point returns a known
        error
        """
        headers = {USER_ID_KEYWORD: 10}
        mocked_request.headers = headers

        user = Users(absolute_uid=10, classic_cookie='ef9df8ds', classic_mirror='mirror.com')
        db.session.add(user)
        db.session.commit()

        mocked_get.side_effect = Timeout

        url = url_for('classiclibraries')

        r = self.client.get(url)

        self.assertStatus(r, CLASSIC_TIMEOUT['code'])
        self.assertEqual(r.json['error'], CLASSIC_TIMEOUT['message'])

    @mock.patch('classic.views.request')
    def test_get_libraries_when_ads_classic_returns_non_200(self, mocked_request):
        headers = {USER_ID_KEYWORD: 10}
        mocked_request.headers = headers

        user = Users(absolute_uid=10, classic_cookie='ef9df8ds', classic_mirror='mirror.com')
        db.session.add(user)
        db.session.commit()

        url = url_for('classiclibraries')
        with HTTMock(ads_classic_fail):
            r = self.client.get(url)

        self.assertStatus(r, CLASSIC_UNKNOWN_ERROR['code'])
        self.assertEqual(r.json['error'], CLASSIC_UNKNOWN_ERROR['message'])

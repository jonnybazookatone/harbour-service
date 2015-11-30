"""
Test webservices
"""
import mock

from flask.ext.testing import TestCase
from flask import url_for
from classic import app
from classic.http_errors import CLASSIC_AUTH_FAILED, CLASSIC_DATA_MALFORMED, CLASSIC_TIMEOUT, CLASSIC_BAD_MIRROR,\
    CLASSIC_NO_COOKIE, CLASSIC_UNKNOWN_ERROR, MYADS_TIMEOUT, MYADS_UNKNOWN_ERROR
from stub_response import ads_classic_200, ads_classic_unknown_user, ads_classic_wrong_password, ads_classic_no_cookie, ads_classic_fail, myads_200, myads_fail
from httmock import HTTMock
from requests.exceptions import Timeout


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

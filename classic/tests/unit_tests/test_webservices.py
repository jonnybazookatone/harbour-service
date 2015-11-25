"""
Test webservices
"""
import mock

from classic import app
from flask.ext.testing import TestCase
from flask import url_for

stub_classic_success = {
    "email": "roman.chyla@gmail.com",
    "cookie": "50eefa48dc",
    "tmp_cookie": "",
    "openurl_srv": "",
    "openurl_icon": "",
    "loggedin": "1",
    "myadsid": "352401271",
    "lastname": "",
    "firstname": "",
    "fullname": "",
    "message": "LOGGED_IN",
    "request": {
        "man_cookie": "",
        "man_email": "roman.chyla@gmail.com",
        "man_nemail": "",
        "man_passwd": "******",
        "man_npasswd": "",
        "man_vpasswd": "",
        "man_name": "",
        "man_url": "http://adsabs.harvard.edu",
        "man_cmd": "4"
        }
}


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
        return app_

    @mock.patch('classic.views.requests.post',  mock.MagicMock(return_value=stub_classic_success))
    def test_authenticating_workflow(self, mocked_request):
        """
        Tests the overall workflow of a user authenticating their ADS credentials via the web app
        """

        # 1. The user fills in their credentials
        #    - email
        #    - password
        #    - mirror
        user_data = {
            'classic_email': 'user@ads.com',
            'classic_password': 'password',
            'mirror': 'mirror'
        }

        # 2. The user submits their credentials to the end point
        url = url_for('AuthenticatedUser'.lower())
        r = self.client.post(url, json=user_data)
        self.assertStatus(r, 200)

        # 3. The webservice contacts the external ADS classic end point to confirm the credentials are correct
        # 4. If the credentials are correct, they are stored in myADS
        mocked_request.assert_has_calls(
            mock.call(['http://adsabs.harvard.edu']),
            mock.call(['http://api.adsabs.harvard.edu/v1/vault/user-data'])
        )

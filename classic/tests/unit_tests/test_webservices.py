"""
Test webservices
"""
import mock

from classic import app
from flask.ext.testing import TestCase
from flask import url_for


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

    def test_authorise_endpoint(self):
        """
        Test basic functionality of the GithubListener endpoint
        """
        url = url_for('AuthenticateUser'.lower())
        r = self.client.get(url)
        self.assertStatus(r, 200)

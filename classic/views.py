"""
Views
"""

import requests

from flask import current_app, request, abort
from flask.ext.restful import Resource


class AuthenticateUser(Resource):
    """
    End point to authenticate the user's ADS classic credentials with the external ADS Classic end point
    """

    def post(self):
        """
        HTTP POST request that receives the user's ADS Classic credentials, and then contacts the Classic system to
        check that what the user provided is indeed valid. If valid, the users ID is stored within the myADS service
        store.

        Post body:
        ----------
        KEYWORD, VALUE
        classic_email: <string> ADS Classic e-mail of the user
        classic_password: <string> ADS Classic password of the user
        classic_mirror: <string> ADS Classic mirror this user belongs to

        Return data:
        -----------
        classic_authed: <boolean> were they authenticated
        classic_email: <string> e-mail that authenticated correctly, empty string on fail

        HTTP Responses:
        --------------
        Succeed authentication: 200
        Fail authentication: 404
        """
        pass

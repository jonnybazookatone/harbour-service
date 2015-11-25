"""
Views
"""

from flask import current_app, request, abort
from flask.ext.restful import Resource


class AuthenticateUser(Resource):
    """
    End point to authenticate the user's ADS classic credentials with the external ADS Classic end point
    """

    def get(self):
        pass

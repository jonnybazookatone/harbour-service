"""
Views
"""

import requests
import traceback

from client import client
from utils import get_post_data, err
from flask import current_app, request
from flask.ext.restful import Resource
from flask.ext.discoverer import advertise
from http_errors import CLASSIC_AUTH_FAILED, CLASSIC_DATA_MALFORMED, CLASSIC_TIMEOUT, CLASSIC_BAD_MIRROR, \
    CLASSIC_NO_COOKIE, CLASSIC_UNKNOWN_ERROR, MYADS_TIMEOUT, MYADS_UNKNOWN_ERROR


class AuthenticateUser(Resource):
    """
    End point to authenticate the user's ADS classic credentials with the external ADS Classic end point
    """

    decorators = [advertise('scopes', 'rate_limit')]
    scopes = ['user']
    rate_limit = [1000, 60*60*24]

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

        Return data (on succeed):
        -------------------------
        classic_authed: <boolean> were they authenticated
        classic_email: <string> e-mail that authenticated correctly

        HTTP Responses:
        --------------
        Succeed authentication: 200
        Bad/malformed data: 400
        User unknown/wrong password/failed authentication: 404
        myADS/ADS Classic times out: 504
        myADS/ADS Classic give unknown messages: 500

        Any other responses will be default Flask errors
        """
        post_data = get_post_data(request)

        # Collect the username, password from the request
        try:
            classic_email = post_data['classic_email']
            classic_password = post_data['classic_password']
            classic_mirror = post_data['classic_mirror']
        except KeyError:
            current_app.logger.warning('User did not provide a required key: {}'.format(traceback.print_exc()))
            return err(CLASSIC_DATA_MALFORMED)

        # Check that the mirror exists and not man-in-the-middle
        if classic_mirror not in current_app.config['ADS_CLASSIC_MIRROR_LIST']:
            current_app.logger.warning('User "{}" tried to use a mirror that does not exist: "{}"'
                                       .format(classic_email, classic_mirror))
            return err(CLASSIC_BAD_MIRROR)

        # Create the correct URL
        url = current_app.config['ADS_CLASSIC_URL'].format(
            mirror=classic_mirror,
            email=classic_email,
            password=classic_password
        )

        # Authenticate
        current_app.logger.info('User "{email}" trying to authenticate at mirror "{mirror}"'
                                .format(email=classic_email, mirror=classic_mirror))
        try:
            response = requests.post(url)
        except requests.exceptions.Timeout:
            current_app.logger.warning('ADS Classic end point timed out, returning to user')
            return err(CLASSIC_TIMEOUT)

        if response.status_code >= 500:
            message, status_code = err(CLASSIC_UNKNOWN_ERROR)
            message['ads_classic'] = {
                'message': response.text,
                'status_code': response.status_code
            }
            current_app.logger.warning('ADS Classic has responded with an unknown error: {}'.format(response.text))
            return message, status_code

        # Sanity check the response
        email = response.json()['email']
        if email != classic_email:
            current_app.logger.warning('User email "{}" does not match ADS return email "{}"'
                                       .format(classic_email, email))
            return err(CLASSIC_AUTH_FAILED)

        # Respond to the user based on whether they were successful or not
        if response.status_code == 200 and response.json()['message'] == 'LOGGED_IN' and int(response.json()['loggedin']):
            current_app.logger.info('Authenticated successfully "{email}" at mirror "{mirror}"'
                                    .format(email=classic_email, mirror=classic_mirror))

            # Save cookie in myADS
            try:
                cookie = response.json()['cookie']
            except KeyError:
                current_app.logger.warning('Classic returned no cookie, cannot continue: {}'.format(response.json()))
                return err(CLASSIC_NO_COOKIE)

            myads_payload = {'classic_cookie': cookie}
            try:
                myads_response = client().post(current_app.config['CLASSIC_MYADS_USER_DATA_URL'], data=myads_payload)
            except requests.exceptions.Timeout:
                current_app.logger.warning('myADS end point timed out, returning to user')
                return err(MYADS_TIMEOUT)

            if myads_response.status_code != 200:
                current_app.logger.warning('myADS end point returned unknown error: "{}", {}'
                                           .format(myads_response.text, myads_response.status_code))
                message, status_code = err(MYADS_UNKNOWN_ERROR)

                message['myads'] = {
                    'message': myads_response.text,
                    'status_code': int(myads_response.status_code)
                }

                return message, status_code

            current_app.logger.info('Successfully saved content for "{}" to myADS: {{"cookie": "{}"}}'
                                    .format(classic_email, '*'*len(myads_response.json()['classic_cookie'])))

            return {
                'classic_email': email,
                'classic_authed': True
            }, 200
        else:
            current_app.logger.warning('Credentials for "{email}" did not succeed at mirror "{mirror}"'
                                       .format(email=classic_email, mirror=classic_mirror))
            return err(CLASSIC_AUTH_FAILED)

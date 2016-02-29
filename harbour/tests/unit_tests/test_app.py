"""
Test webservices
"""

import mock
import json
import boto3

from unittest import TestCase
from moto import mock_s3
from harbour.app import create_app


class TestApp(TestCase):
    """
    Test the application, such things as create_app
    """

    @mock_s3
    def test_load_s3_create_app_mongo_load_success(self):
        """
        Test that when the application is created, that the mongo user data
        is loaded from s3, if available.
        """
        stub_mongogut_users = {
            'user@ads.com': 'cb16a523-cdba-406b-bfff-edfd428248be.json'
        }

        s3_resource = boto3.resource('s3')
        s3_resource.create_bucket(Bucket='adsabs-mongogut')
        bucket = s3_resource.Bucket('adsabs-mongogut')

        # First is libraries
        bucket.put_object(
            Key='users.json',
            Body=json.dumps(stub_mongogut_users)
        )

        app = create_app()

        self.assertTrue(app.config['ADS_TWO_POINT_OH_LOADED_USERS'])
        self.assertEqual(
            app.config['ADS_TWO_POINT_OH_USERS'],
            stub_mongogut_users
        )

    @mock.patch('harbour.app.boto3.resource')
    def test_load_s3_create_app_mongo_load_success(self, mock_resource):
        """
        Test that when the application is created, that the mongo user data
        is loaded from s3, if available.
        """
        mock_resource.side_effect = Exception

        app = create_app()

        self.assertFalse(app.config['ADS_TWO_POINT_OH_LOADED_USERS'])
        self.assertEqual(app.config['ADS_TWO_POINT_OH_USERS'], {})

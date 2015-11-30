"""
Mock responses to be used with HTTMock
"""

from httmock import urlmatch
from stub_data import stub_classic_success, stub_classic_unknown_user, stub_classic_wrong_password, \
    stub_classic_no_cookie


@urlmatch(netloc=r'(.*\.)?mirror\.com')
def ads_classic_200(url, request):
    return {
        'status_code': 200,
        'content': stub_classic_success
    }


@urlmatch(netloc=r'(.*\.)?mirror\.com')
def ads_classic_unknown_user(url, request):
    return {
        'status_code': 404,
        'content': stub_classic_unknown_user
    }


@urlmatch(netloc=r'(.*\.)?mirror\.com')
def ads_classic_wrong_password(url, request):
    return {
        'status_code': 404,
        'content': stub_classic_wrong_password
    }


@urlmatch(netloc=r'(.*\.)?mirror\.com')
def ads_classic_no_cookie(url, request):
    return {
        'status_code': 200,
        'content': stub_classic_no_cookie
    }


@urlmatch(netloc=r'(.*\.)?mirror\.com')
def ads_classic_fail(url, request):
    return {
        'status_code': 500,
        'content': 'Unknown error'
    }


@urlmatch(netloc=r'(.*\.)?myads\.net')
def myads_200(url, request):
    return {
        'status_code': 200,
        'content': {'classic_cookie': 'g8gfdgfhd'}
    }


@urlmatch(netloc=r'(.*\.)?myads\.net')
def myads_fail(url, request):
    return {
        'status_code': 500,
        'content': 'Unknown error'
    }
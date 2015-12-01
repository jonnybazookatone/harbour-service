# encoding: utf-8
"""
Stub data for all the tests
"""

stub_classic_success = {
    "email": "user@ads.com",
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

stub_classic_unknown_user = {
      "email": "",
      "cookie": "54050f19fa",
      "tmp_cookie": "",
      "openurl_srv": "",
      "openurl_icon": "",
      "loggedin": "0",
      "myadsid": "0",
      "lastname": "",
      "firstname": "",
      "fullname": "",
      "message": "ACCOUNT_NOTFOUND",
      "request": {
          "man_cookie": "",
          "man_email": "roman.chyla@gmail.comssssss",
          "man_nemail": "",
          "man_passwd": "******",
          "man_npasswd": "",
          "man_vpasswd": "",
          "man_name": "",
          "man_url": "",
          "man_cmd": "4"
       }
}

stub_classic_wrong_password = {
      "email": "ads@user.com",
      "cookie": "50eefa48dc",
      "tmp_cookie": "",
      "openurl_srv": "",
      "openurl_icon": "",
      "loggedin": "0",
      "myadsid": "352401271",
      "lastname": "",
      "firstname": "",
      "fullname": "",
      "message": "WRONG_PASSWORD",
      "request": {
          "man_cookie": "",
          "man_email": "ads@user.com",
          "man_nemail": "",
          "man_passwd": "********",
          "man_npasswd": "",
          "man_vpasswd": "",
          "man_name": "",
          "man_url": "",
          "man_cmd": "4"
       }
}

stub_classic_no_cookie = {
    "email": "user@ads.com",
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

stub_classic_libraries_success = {
    'count': '2',
    'libraries': [
        {
            'desc': 'Description',
            'entries': [
                {
                    'bibcode': '2015MNRAS.446.4239E'
                },
                {
                    'bibcode': '2015A&C....10...61E'
                },
                {
                    'bibcode': '2014A&A...562A.100E'
                },
                {
                    'bibcode': '2013A&A...556A..23E'
                }
            ],
            'lastmod': '01-Dec-2015',
            'name': 'Name'
        }
    ],
    'owner': 'Owner',
    'pubid': 'ID',
    'status': {
        'cookie': 'ef9df8ds',
        'libfile': '/file/on/disk',
        'query_string': 'cookie=ef9df8ds',
        'server': 'server',
        'timestamp': 'Tue Dec  1 11:37:39 2015'
    },
    'uid': 'ID'
}

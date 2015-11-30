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

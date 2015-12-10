[![Build Status](https://travis-ci.org/adsabs/harbour-service.svg?branch=master)](https://travis-ci.org/adsabs/harbour-service)
[![Coverage Status](https://coveralls.io/repos/adsabs/harbour-service/badge.svg?branch=master&service=github)](https://coveralls.io/github/adsabs/harbour-service?branch=master)
[![Code Climate](https://codeclimate.com/github/adsabs/harbour-service/badges/gpa.svg)](https://codeclimate.com/github/adsabs/harbour-service)
[![Issue Count](https://codeclimate.com/github/adsabs/harbour-service/badges/issue_count.svg)](https://codeclimate.com/github/adsabs/harbour-service)

# harbour-service

Gateway service for all your ADS communication with legacy systems, such as Classic and BEER/2.0

# ADS Classic Workflow

1. User enters their 'email', 'password', and 'mirror' for their ADS credentials
  ```bash
  user> curl -X POST 'http://api/v1/harbour/auth' -H 'Authorization: Bearer <TOKEN>' 
  --data '{"classic_email": "email", "classic_password": "password", "classic_mirror": "mirror"}'
  
  200, {"classic_email": "email", "classic_mirror": "mirror", "classic_authed": true}
  ```

1. If the user does not know the mirror, they can access a list of available mirrors for the service
  ```bash
  user> curl -X GET 'http://api/v1/harbour/mirrors' -H 'Authorization: Bearer <TOKEN>'
  
  200, ['site1', 'site2', ...., 'siteN']
  ```

1. User wants to check the credentials they have stored
  ```bash
  user> curl -X GET 'http://api/v1/harbour/user' -H 'Authorization: Bearer <TOKEN>'
  
  200, {"classic_email": "email", "classic_mirror": "mirror"}
  ```

1. User imports the libraries from ADS Classic
  ```bash
  user> curl -X GET 'http://api/v1/biblib/classic' -H 'Authorization: Bearer <TOKEN>'
  
  200, [{"action": "created", "library_id": "fdsfsfsdfdsfds", "name": "Name", "num_added": 4, "description": "Description"}, {"action": "created", "library_id": "dsadsadsadsa", "name": "Name2", "n
um_added": 4, "description": "Description2"}]
  ```

*Notes*
The mirror they can use must be in the list defined in `config.py`.


# Development

You can run unit tests in the following way:
```bash
nosetests harbour/tests/
```

A Vagrantfile and puppet manifest are available for development within a virtual machine. To use the vagrant VM defined here you will need to install *Vagrant* and *VirtualBox*. 

  * [Vagrant](https://docs.vagrantup.com)
  * [VirtualBox](https://www.virtualbox.org)

To load and enter the VM: `vagrant up && vagrant ssh`

[![Build Status](https://travis-ci.org/adsabs/harbour-service.svg?branch=master)](https://travis-ci.org/adsabs/harbour-service)
[![Coverage Status](https://coveralls.io/repos/adsabs/harbour-service/badge.svg?branch=master&service=github)](https://coveralls.io/github/adsabs/harbour-service?branch=master)
[![Code Climate](https://codeclimate.com/github/adsabs/harbour-service/badges/gpa.svg)](https://codeclimate.com/github/adsabs/harbour-service)
[![Issue Count](https://codeclimate.com/github/adsabs/harbour-service/badges/issue_count.svg)](https://codeclimate.com/github/adsabs/harbour-service)

# harbour-service

Gateway service for all your ADS communication with legacy systems, such as Classic and BEER/2.0

# Development

You can run unit tests in the following way:
```bash
nosetests classic/tests/
```

A Vagrantfile and puppet manifest are available for development within a virtual machine. To use the vagrant VM defined here you will need to install *Vagrant* and *VirtualBox*. 

  * [Vagrant](https://docs.vagrantup.com)
  * [VirtualBox](https://www.virtualbox.org)

To load and enter the VM: `vagrant up && vagrant ssh`

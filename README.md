[![Build Status](https://travis-ci.org/jonnybazookatone/classic-service.svg?branch=master)](https://travis-ci.org/jonnybazookatone/classic-service)
[![Coverage Status](https://coveralls.io/repos/jonnybazookatone/classic-service/badge.svg?branch=master&service=github)](https://coveralls.io/github/jonnybazookatone/classic-service?branch=master)

# Classic-service

Gateway service for all your ADS classic needs

# Development

You can run unit tests in the following way:
```bash
nosetests classic/tests/
```

A Vagrantfile and puppet manifest are available for development within a virtual machine. To use the vagrant VM defined here you will need to install *Vagrant* and *VirtualBox*. 

  * [Vagrant](https://docs.vagrantup.com)
  * [VirtualBox](https://www.virtualbox.org)

To load and enter the VM: `vagrant up && vagrant ssh`

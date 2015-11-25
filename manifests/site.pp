# Some const. variables
$path_var = '/usr/bin:/usr/sbin:/bin:/usr/local/sbin:/usr/sbin:/sbin'
$build_packages = ['python', 'python-dev', 'python-pip', 'git', 'libpq-dev', 'ipython', 'postgresql-client-9.3']
$pip_requirements = '/vagrant/requirements.txt'

# Update package list
exec {'apt_update_1':
  command => 'apt-get update && touch /etc/.apt-updated-by-puppet1',
  creates => '/etc/.apt-updated-by-puppet1',
  path => $path_var,
}

# Install packages
package {$build_packages:
  ensure => installed,
  require => Exec['apt_update_1'],
}

# Upgrade pip
exec {'upgrade_pip':
  command => 'pip install --upgrade pip',
  require => Package[$build_packages],
  path => $path_var,
}

# Install all python dependencies for selenium and general software
exec {'pip_install_modules':
  command => 'pip install -r /vagrant/requirements.txt',
  logoutput => on_failure,
  path => $path_var,
  tries => 2,
  timeout => 1000, # This is only require for Scipy/Matplotlib - they take a while
  require => Exec['upgrade_pip'],
}

Exec['apt_update_1'] -> Package[$build_packages] -> Exec['upgrade_pip'] -> Exec['pip_install_modules']

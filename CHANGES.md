# Change Log
All notable changes to the config fileswill be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

## [1.0.5] - 2016-03-11
### Added

  * Authentication end point of ADS 2.0 users, stores email on success

### Changes

  * End points updated to have separate classic and 2.0 auth end points
  * Extra logic added due to the exta fields in the model
  * Models updated to include ADS 2.0 e-mail - migration of database
  * README.md updated for new end point names

## [1.0.4] - 2016-03-09
### Added
  
  * Ability to export ADS2.0 library to Zotero format, in a zip file
  * Tests included

## [1.0.3] - 2016-03-01
### Added

  * Ability to import ADS2.0 libraries from flat files from AWS S3
  * Tests for the new end points

### Changed
  * Naming of the end points

## [1.0.2] - 2015-12-08
### Added

  * A new end point that returns the list of mirrors this service allows
  * Tests for the new end point

### Changed

  * Updated documentation on the workflow

## [1.0.1] - 2015-12-07
### Added

  * CHANGES.md file
  * Migration and database creation scripts
  * File for base class for tests
  * Tests for manage scripts

### Changed

  * Renamed some of the configuration keys

## [1.0.0] - 2015-12-07
### Added

  * First release of harbour service



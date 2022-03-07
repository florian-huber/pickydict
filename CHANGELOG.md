# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2022-03-07

### Changed

- does not raise an exception anymore (but a warning) when the initial dictionary passed to PickyDict contains duplicate keys (after key conversion). If duplicate keys exist, only the value for the desired key will be kept [#11](https://github.com/florian-huber/pickydict/pull/11)

### Fixed

- ensure that PickyDict object can be pickled [#9](https://github.com/florian-huber/pickydict/pull/9)

## [0.3.0] - 2022-02-09

### Added

- `copy()` method to create shallow copy of PickyDict [#4](https://github.com/florian-huber/pickydict/pull/4)

### Changed

- expanded unit tests

## [0.2.0] - 2022-01-06

### Changed:

- Switch parent class from `UserDict` to `dict` to also allow `json.dumbs()` of PickyDict objects.
- Added `.to_json()` method that will turn the main dictionary into json.

## [0.1.2] - 2022-01-06

### Changed

- Updated documentation and version fix.

## [0.1.1] - 2022-01-06

### Changed

- Updated documentation.

## [0.1.0] - 2022-01-06

### Added

- This is the initial version of PickyDict

[Unreleased]: https://github.com/florian-huber/pickydict/compare/0.4.0...HEAD
[0.4.0]: https://github.com/florian-huber/pickydict/0.3.0...0.4.0
[0.3.0]: https://github.com/florian-huber/pickydict/0.2.0...0.3.0
[0.2.0]: https://github.com/florian-huber/pickydict/0.1.2...0.2.0
[0.1.2]: https://github.com/florian-huber/pickydict/0.1.1...0.1.2
[0.1.1]: https://github.com/florian-huber/pickydict/0.1.0...0.1.1
[0.1.0]: https://github.com/florian-huber/pickydict/releases/tag/0.1.0

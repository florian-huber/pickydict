# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `copy()` method to create shallow copy of PickyDict [#4](https://github.com/florian-huber/pickydict/pull/4)


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

[Unreleased]: https://github.com/florian-huber/pickydict/compare/0.2.0...HEAD
[0.2.0]: https://github.com/florian-huber/pickydict/0.1.2...0.2.0
[0.1.2]: https://github.com/florian-huber/pickydict/0.1.1...0.1.2
[0.1.1]: https://github.com/florian-huber/pickydict/0.1.0...0.1.1
[0.1.0]: https://github.com/florian-huber/pickydict/releases/tag/0.1.0

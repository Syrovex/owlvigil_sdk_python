# Changelog

This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and uses [Semantic Versioning](https://semver.org/). During the 0.x preview,
minor releases may include announced breaking changes.

## [Unreleased]

### Added

- A generated, checked-in Management OpenAPI catalog with 144 operations and
  generated snake_case sync/async methods.
- Generated Python `TypedDict` definitions for 167 Management schemas.
- Management `open_api()` requests with typed path/query/body forwarding and
  cursor-based workspace iteration.
- Sync and async OAuth 2.0 clients with custom base paths and consistent
  protocol errors.
- Production, staging, and local environment routing compatible with the Go
  SDK.

### Changed

- Direct `pytest` execution now works with the src-layout package.
- CI validates the source package, wheel/sdist metadata, and generated API
  surface.

# Changelog

## 0.2.0 (2026-04-29)

- Add `Spinner.info()` finisher (cyan ⓘ symbol) for parity with `succeed`/`fail`/`warn`
- Replace import-only stub with real test suite covering lifecycle, context manager, decorator, finishers, and thread safety

## 0.1.7 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.1.6

- Add pytest and mypy tool configuration to pyproject.toml

## 0.1.5

- Add basic import test

## 0.1.4

- Add Development section to README

## 0.1.1

- Re-release for PyPI publishing

## 0.1.0 (2026-03-15)

- Initial release
- Spinner class with start/stop/succeed/fail/warn/update methods
- Context manager support via `spinner()` factory
- Decorator support via `spin()`
- Five built-in styles: dots, line, bounce, braille, arrow
- Auto-detect non-TTY environments
- Thread-safe animation with background thread

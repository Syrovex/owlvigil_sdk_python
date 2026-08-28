# Contributing to OwlVigil

Thank you for improving the OwlVigil SDK.

## Development

Use Python 3.9 or later in a virtual environment.

```bash
python -m pip install -e '.[test]'
pytest
```

Keep changes focused, add contract tests for public behavior, and never add API
keys, access tokens, provider credentials, or webhook secrets to commits.

Open an issue before making a large API or compatibility change. Pull requests
should explain the affected API contract, tests run, compatibility impact, and
any credential requirements. By contributing, you agree that your contribution
is licensed under this repository's MIT License.

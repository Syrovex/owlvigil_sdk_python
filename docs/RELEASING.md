# Releasing

1. Create the `owlvigil` PyPI project, connect this repository as a trusted
   publisher, and protect the `pypi` GitHub environment.
2. Update `pyproject.toml`, `owlvigil.__version__`, the public User-Agent
   version, README, and `CHANGELOG.md` in one reviewed pull request.
3. Run the full test matrix, build sdist and wheel, and run `twine check`.
4. Merge the release commit and create the matching signed tag, such as
   `v0.2.0`. The Release workflow publishes through PyPI OIDC.
5. Verify installation from PyPI and complete the GitHub release notes.

Do not create or store a long-lived PyPI token when trusted publishing is
available.

# Contributing to HR Analytics Dashboard

Thank you for your interest in contributing! Here's how to get involved.

## How to Contribute

### Reporting Bugs
Open an issue with the label `bug`. Include:
- Steps to reproduce
- Expected vs. actual behavior
- Power BI Desktop version and OS

### Suggesting Enhancements
Open an issue with the label `enhancement`. Describe the use case and proposed solution.

### Submitting Changes

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** — keep commits atomic and well-described
4. **Run validation**: `python src/data_validation.py`
5. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation only
   - `refactor:` code change that doesn't add a feature or fix a bug
   - `data:` changes to sample data or schema
6. **Push**: `git push origin feature/your-feature-name`
7. **Open a Pull Request** against `main`

## DAX Contribution Guidelines

- Add every new measure to `docs/DAX_MEASURES.md` with a description and example
- Prefix measure names with the domain (e.g., `Recruitment - `, `Attrition - `) for large measure tables
- Avoid circular dependencies — test with a simple card visual before committing

## Python Contribution Guidelines

- Follow PEP 8
- Add docstrings to all functions
- Keep functions under 50 lines; break larger logic into helpers
- Add a `if __name__ == "__main__"` block for any runnable script

## Questions?

Open a Discussion in the GitHub Discussions tab.

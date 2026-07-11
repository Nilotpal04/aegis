# Contributing to Aegis

First of all. thank you for considering contributing to Aegis!

Whether it's fixing a bug, improving documentation, suggesting a feature, or implementing a new algorithm, every contribution is appreciated.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/Nilotpal04/aegis.git
cd aegis
```

Install the project dependencies:

```bash
uv sync
```

## Running Tests

Run the full test suite:

```bash
pytest
```

## Code Style

Before opening a pull request, make sure your code is formatted and passes linting.

Format the code:

```bash
black .
```

Lint the project:

```bash
ruff check .
```

## Commit Messages

Please use clear and descriptive commit messages.

## Pull Requests

Before submitting a pull request, please ensure that:

- Your code passes all tests.
- New features include appropriate tests.
- Documentation is updated if necessary.
- Code is formatted with Black.
- Linting passes with Ruff.

## Reporting Issues

If you find a bug or have a feature request, please open a GitHub Issue with:

- A clear description
- Steps to reproduce (if applicable)
- Expected behavior
- Actual behavior
- Environment details (Python version, Redis version, OS)

## Project Goals

Aegis aims to be:

- Easy to use
- Easy to extend
- Production-inspired
- Well tested
- Well documented

Contributions that improve reliability, performance, documentation, developer experience, or add new backends and algorithms are always welcome.

Thank you for helping make Aegis better! 🚀
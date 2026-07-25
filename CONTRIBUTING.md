# Contributing to ObfBot

First off, thanks for considering contributing to ObfBot! It's people like you that make it such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details** (Python version, OS, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior** and **the expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python style guide
* End all files with a newline
* Use meaningful commit messages

## Development Setup

```bash
# Clone the repo
git clone https://github.com/nevawork/obfbot.git
cd obfbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run the bot
python -m bot.bot
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest tests/
```

## Style Guide

This project follows PEP 8 style guide with some exceptions:

* Use meaningful variable names
* Maximum line length: 100 characters
* Use type hints where appropriate
* Add docstrings to all functions and classes

### Code Quality Tools

```bash
# Format code
black bot/

# Lint code
pylint bot/

# Type check
mypy bot/
```

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example:
```
Add identifier renaming protection module

Implement scope-aware variable renaming with random identifier
generation. Adds support for preserving reserved keywords and
library functions.

Fixes #42
```

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed

## Recognition

Contributors will be recognized in the README and release notes.

Thank you for contributing! 🎉

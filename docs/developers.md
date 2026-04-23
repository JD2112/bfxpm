---
hide:
  - navigation
---

# For Developers

We welcome contributions from the bioinformatics community! Whether you are fixing bugs, adding new CLI commands, or improving documentation, this guide will help you set up your local development environment to work on **BfxPM**.

## 1. Setting Up the Development Environment

To start developing, clone the repository and install the package along with its development dependencies (`pytest`) in "editable" mode. We highly recommend doing this inside a virtual environment.

```bash
# Clone the repository
git clone https://github.com/JD2112/bfxpm.git
cd bfxpm

# Create and activate a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install BfxPM in editable mode along with dev dependencies
python3 -m pip install -e ".[dev]"
```

By installing in *editable mode* (`-e`), any changes you make to the source code in `src/bfxpm/` will take effect immediately without needing to reinstall the package. 

*(Note: Older versions of pip may fail to install `pyproject.toml` packages in editable mode without a `setup.py`. If this occurs, simply upgrade pip using `python3 -m pip install --upgrade pip`.)*

## 2. Running the Test Suite

BfxPM uses [**pytest**](https://pytest.org) as its testing framework. 

To run the full test suite, simply execute:
```bash
# Ensure you are at the project root
PYTHONPATH=src python3 -m pytest tests/
```

### Why Pytest? Do I need Unittest?

You **do not** need to install `unittest`. 

- `unittest` is built into Python natively.
- `pytest` is fully backwards compatible and can run both standard `pytest` fixtures (which we use for `test_main.py`) as well as traditional `unittest.TestCase` classes.

You have the freedom to write your tests using whichever paradigm you are most comfortable with. As long as your test files begin with `test_` or end with `_test.py`, `pytest` will find and execute them.

## 3. Submitting Your Changes

1. **Test your code**: Ensure all existing tests (and any new tests you write) pass successfully using the command above.
2. **Follow the formatting**: We follow standard Python formatting (PEP 8). Try to keep your code clean and readable.
3. **Commit your changes**: Please write clear, concise commit messages.
4. **Push and create a Pull Request**: Submit your pull request to the `main` branch. 

For a complete breakdown of code review expectations and code of conduct, please fully read the [Contributing Guidelines](https://github.com/JD2112/bfxpm/blob/main/CONTRIBUTING.md) in the root of the repository.

---

**Thank you for helping us build better tools for Bioinformaticians!** :black_heart:

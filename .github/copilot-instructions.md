# Copilot Instructions for hebikata

## Project Overview

**hebikata** is a self-hosted Python e-learning platform built with Streamlit. It teaches Python through repetition-based learning (inspired by karate kata), where students practice exercises 5 times with different variations to build mastery.

The project is currently in early planning stages - the `app/` and `data/` directories mentioned in README.md do not yet exist. Core infrastructure (dependencies, docs setup, utility scripts) is in place.

## Architecture

### Current Structure

```
hebikata/
├── hebikata.py          # Empty placeholder (main app logic TBD)
├── vistree.py           # Utility: generates directory tree visualization
├── docs/                # Sphinx documentation setup
│   ├── source/conf.py   # Sphinx config; expects source in ../app/
│   └── source/index.rst # Docs skeleton (not yet populated)
├── requirements.txt     # Full dependency list including Streamlit, pytest, ruff, black, mypy
└── vistree.bat          # Windows batch script for vistree.py
```

### Planned Structure (from README.md)

```
app/       # Core Streamlit app, UI components, exercises, pytest tests
data/      # Exercise variations and hints (JSON files)
scripts/   # Dev and deployment helpers
```

### Key Dependencies

- **UI**: Streamlit 1.45.1
- **Testing**: pytest 8.3.5, pytest-cov 6.1.1
- **Code Quality**: ruff 0.11.11, black 25.1.0, mypy 1.15.0
- **Docs**: Sphinx 8.2.3, sphinx-rtd-theme 3.0.2

### Dependency Management

This project uses **uv** for fast, reliable Python package management. Install dependencies with:

```bash
# Install dependencies from requirements.txt
uv pip install -r requirements.txt

# Or create/sync a virtual environment
uv venv
uv pip sync requirements.txt
```

## Development Commands

### Running the App

```bash
streamlit run app/main.py
```

*Note: This will fail until `app/main.py` is created.*

### Documentation

```bash
# Build HTML documentation (from docs/ directory)
cd docs
make html               # Unix/macOS
make.bat html           # Windows

# View built docs at docs/build/html/index.html
```

### Code Quality

No project-specific configuration files exist yet (no `pyproject.toml`, `ruff.toml`, etc.). Use tool defaults:

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .

# Run tests (once tests exist)
pytest
pytest -v                    # Verbose output
pytest path/to/test_file.py  # Single test file
pytest -k test_name          # Single test by name
pytest --cov                 # With coverage
```

## Project Conventions

### Python Code Style

- **PEP 8 compliance** is required (enforced by black and ruff)
- **Type hints** are expected (checked by mypy)
- Focus on **Pythonic idioms** and **clean code principles**
- All code must be suitable for educational content (clear, well-commented, exemplary)

### Pedagogical Focus

When creating exercises or app features:

- **Repetition with variation**: Each concept should be practiced multiple times with different inputs
- **Immediate feedback**: Automated testing must provide clear, actionable error messages
- **Progressive difficulty**: Build from simple to complex incrementally
- **Real-world framing**: Exercises should feel like practical programming tasks, not toy problems

### Documentation

- Use **Google or NumPy style docstrings** (configured in Sphinx conf.py with napoleon extension)
- All public functions/classes must be documented
- Sphinx autodoc will generate API docs from docstrings

## When Creating New Directories

The project expects `app/`, `data/`, and `scripts/` directories per README.md. When creating these:

1. **app/** should contain:
   - `main.py` as the Streamlit entry point
   - Modular components (UI, exercises, test validation logic)
   - Pytest tests in test files (`test_*.py` or `*_test.py`)

2. **data/** should contain:
   - JSON files with exercise variations and hints
   - Follow a consistent schema for exercise definitions

3. **scripts/** should contain:
   - Development utilities (setup, data generation, deployment helpers)
   - Keep scripts platform-agnostic where possible

## Utility Scripts

### vistree.py

Generates directory tree visualizations, respecting `.gitignore` rules:

```bash
python vistree.py
# Outputs: vistree.txt (ASCII tree) and structure.dot (Graphviz format)
```

Excludes `.git/`, `venv/`, and gitignored patterns automatically.

## Adding Dependencies

Use `uv` to add new packages:

```bash
# Add a new package
uv pip install package-name

# Update requirements.txt after adding packages
uv pip freeze > requirements.txt
```

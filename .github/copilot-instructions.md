# Copilot Instructions for hebikata

## Project Overview

**hebikata** is a self-hosted Python e-learning platform built with Streamlit. It teaches Python through repetition-based learning (inspired by karate kata), where students complete exercises 3 times with immediate feedback to build mastery.

The app is fully functional and deployed on Streamlit Cloud.

## Directory Structure

```
hebikata/
├── app/
│   └── main.py              # Single Streamlit page (entry point + UI + execution engine)
├── data/
│   ├── index.yaml           # Ordered registry of exercise refs
│   ├── exercises/*.yaml     # One file per exercise (nested schema)
│   └── solutions/*.py       # Correct code, kept separate from YAML
├── tests/
│   ├── conftest.py          # Fixtures for loading exercises/solutions
│   ├── test_execution_engine.py  # Tests for execute_code_with_tests()
│   ├── test_exercise_data.py     # Validates all exercise YAMLs
│   └── test_exercise_solutions.py # Auto-validates solutions pass their tests
├── research/
│   ├── exercises/           # Exercise design patterns and templates
│   ├── pedagogy/            # Learning theory and references
│   └── results/             # User study data and analysis
├── docs/                    # Sphinx documentation (skeleton, not populated)
├── requirements.txt         # Minimal deploy deps (Streamlit, pytest, pyyaml)
├── requirements-dev.txt     # Includes black, ruff, mypy, pytest-cov, sphinx
├── run_hebikata.bat         # Windows quick launcher
├── vistree.py               # Directory tree visualization utility
└── AGENTS.md                # OpenCode agent instructions
```

## Key Dependencies

- **UI**: Streamlit 1.45.1
- **Testing**: pytest 8.3.5, pytest-cov 6.1.1
- **Code Quality**: ruff 0.11.11, black 25.1.0, mypy 1.15.0
- **Docs**: Sphinx 8.2.3, sphinx-rtd-theme 3.0.2

## Dependency Management

Uses **uv** for package management:

```bash
uv venv
uv pip install -r requirements-dev.txt   # local dev (all tools)
uv pip install -r requirements.txt       # deployment (minimal)
```

## Development Commands

```bash
streamlit run app/main.py                    # Run app at http://localhost:8501
pytest                                       # Run all tests
pytest --cov                                 # With coverage
black .                                      # Format
ruff check .                                 # Lint
mypy .                                       # Typecheck
```

## Exercise Data Structure

Exercises use individual YAML files with a nested schema:

**`data/index.yaml`** — ordered registry:
```yaml
exercises:
  - ref: var_rpg_001
  - ref: var_hack_001
  ...
```

**`data/exercises/{ref}.yaml`** — exercise definition:
```yaml
id: var_rpg_001
metadata:
  chapter: 1
  concept: variables
  subconcept: assignment
  difficulty: beginner
  theme: rpg
  prerequisites: []
  tags: [variables, assignment]
content:
  prompt: |               # shown to the student
  initial_code: |         # starting code with a bug
validation:
  tests: |                # inline test function(s), run via exec()
hints:
  - level: basic
    text: "..."
pep_tip: "..."
boss: false               # true for boss-challenge exercises
```

**`data/solutions/{ref}.py`** — plain Python file with the correct answer code.

## Adding a New Exercise

1. Create `data/exercises/{unique_id}.yaml` with the schema above
2. Create `data/solutions/{unique_id}.py` with the correct code
3. Register it in `data/index.yaml` at the desired position
4. Run `pytest` to validate YAML integrity and solution correctness

## Architecture Notes

- `app/main.py` is a single-page Streamlit app with inline CSS (green-terminal arcade theme)
- Execution engine (`execute_code_with_tests()` at line 64) uses `exec()` in an isolated namespace — no sandboxing
- Session state tracks: successes, attempts, score, lives
- Mastery = 3 successful completions per exercise, 50 points each, 3 lives total
- Tests are inline strings in the exercise YAML, executed via `exec()` not real pytest

## Project Conventions

- PEP 8 compliance (enforced by black + ruff)
- Type hints expected (checked by mypy)
- Google/NumPy-style docstrings (configured in Sphinx conf.py)
- No `pyproject.toml` or tool-specific config exists — all tools use defaults
- No CI/CD workflows configured

## Pedagogical Focus

- **Repetition with variation**: Each concept practiced with different themed inputs
- **Immediate feedback**: Assertions in test code must produce clear error messages
- **Progressive difficulty**: Simple to complex, with prerequisites linking exercises
- **Real-world framing**: Exercises framed as practical tasks (RPG, hacking, science, crypto)

## Deployment

Streamlit Cloud deploys from `main` using `requirements.txt` (dev packages excluded).
Live demo: https://hebikatagit-a96zsajn6ln94t2xfnxpcm.streamlit.app/

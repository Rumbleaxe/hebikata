# Copilot Instructions for hebikata

## Project Overview

**hebikata** is a self-hosted Python e-learning platform built with Streamlit. It teaches Python through repetition-based learning (inspired by karate kata), where students complete exercises 3 times with immediate feedback to build mastery.

The app is fully functional and deployed on Streamlit Cloud.

## Directory Structure

```
hebikata/
├── app/
│   ├── main.py              # Entry point — page config + render_app() call
│   ├── engine.py            # execute_code_with_tests() — exec() in isolated namespace
│   ├── data_loader.py       # load_exercises() — reads index.yaml + per-file YAMLs
│   ├── session.py           # Session state, persistence (localStorage), navigation, hints
│   └── ui.py                # All Streamlit UI, CSS theme, code editor, layout
├── data/
│   ├── index.yaml           # Ordered registry of exercise refs
│   ├── exercises/*.yaml     # One file per exercise (nested schema)
│   └── solutions/*.py       # Correct code, kept separate from YAML
├── tests/
│   ├── conftest.py          # Fixtures for loading exercises/solutions
│   ├── test_execution_engine.py  # Tests for execute_code_with_tests()
│   ├── test_exercise_data.py     # Validates all exercise YAMLs
│   └── test_exercise_solutions.py # Auto-validates solutions pass their tests
├── .github/
│   ├── copilot-instructions.md    # This file
│   └── workflows/ci.yml           # CI: ruff, black, mypy, pytest
├── pyproject.toml            # Project metadata + tool configs
├── requirements.txt          # Minimal deploy deps
├── requirements-dev.txt      # Full dev deps
├── AGENTS.md                 # OpenCode agent instructions
└── run_hebikata.bat          # Windows quick launcher
```

## Key Dependencies

- **UI**: Streamlit >=1.45.1
- **Code Editor**: streamlit-code-editor >=0.1.22
- **Persistence**: streamlit-js-eval >=0.2.70
- **Testing**: pytest >=8.3.5, pytest-cov >=6.1.1
- **Code Quality**: ruff >=0.11.11, black >=25.1.0, mypy >=1.15.0
- **Docs**: Sphinx >=8.2.3, sphinx-rtd-theme >=3.0.2

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
mypy app/                                    # Typecheck
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
  - level: detailed
    text: "..."
  - level: solution
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

- `app/main.py` is a slim entry point that calls `app.ui.render_app()`
- Execution engine (`app/engine.py`) uses `exec()` in an isolated namespace — no sandboxing
- Session state (`app/session.py`) tracks: successes, attempts, score, lives, hint_levels
- Persistence uses browser localStorage via `streamlit-js-eval` (per-browser, no auth)
- UI (`app/ui.py`) uses a purple dark theme with JetBrains Mono font
- Code editor is `streamlit-code-editor` (returns a dict; access code via `response["text"]`)
- Mastery = 3 successful completions per exercise, 50 points each, 3 lives total
- Hints: 3 levels per exercise (basic → detailed → solution), -10 points per hint used
- Tests are inline strings in the exercise YAML, executed via `exec()` not real pytest

## Project Conventions

- PEP 8 compliance (enforced by black + ruff)
- Type hints expected (checked by mypy, Python 3.12 style: `dict` not `Dict`, `X | Y` not `Optional`)
- Tool configs centralized in `pyproject.toml`
- CI runs on push/PR to main via GitHub Actions

## Pedagogical Focus

- **Repetition with variation**: Each concept practiced with different themed inputs
- **Immediate feedback**: Assertions in test code must produce clear error messages
- **Progressive difficulty**: Simple to complex, with prerequisites linking exercises
- **Real-world framing**: Exercises framed as practical tasks (RPG, hacking, science, crypto)

## Deployment

Streamlit Cloud deploys from `main` using `requirements.txt` (dev packages excluded).
Live demo: https://hebikatagit-a96zsajn6ln94t2xfnxpcm.streamlit.app/

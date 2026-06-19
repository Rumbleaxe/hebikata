# AGENTS.md — hebikata

## Quick start
- Setup: `uv venv && uv pip install -r requirements-dev.txt`
- Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
- Run: `streamlit run app/main.py` (or `.\run_hebikata.bat` on Windows)
- Open: http://localhost:8501

## Tests
- `pytest` — runs all 19+ tests in `tests/`
- Coverage: `pytest --cov`
- `tests/test_execution_engine.py` — validates `execute_code_with_tests()` (success, failure, syntax errors, edge cases)
- `tests/test_exercise_data.py` — validates all exercise YAMLs have required fields, valid prereqs, correct types
- `tests/test_exercise_solutions.py` — auto-validates every exercise solution passes its own tests

## Code quality
- Format: `black .`
- Lint: `ruff check .`
- Typecheck: `mypy app/`
- All tool configs in `pyproject.toml`

## Architecture
```
app/
├── main.py         # Entry point — page config + render_app() call
├── engine.py       # execute_code_with_tests() — exec() in isolated namespace
├── data_loader.py  # load_exercises() — reads index.yaml + per-file YAMLs
├── session.py      # Session state, persistence (localStorage), navigation, hints
└── ui.py           # All Streamlit UI, CSS theme, code editor, layout
```

- Entrypoint: `app/main.py` — calls `app.ui.render_app()`
- Execution engine: `app/engine.py` — `execute_code_with_tests()` uses `exec()` in isolated namespace
- Session state: `app/session.py` — manages progress, localStorage persistence, hint system
- UI: `app/ui.py` — purple dark theme, JetBrains Mono font, streamlit-code-editor
- Mastery = 3 successful completions per exercise, 50 points each, 3 lives total
- Hints: 3 levels per exercise (basic → detailed → solution), -10 points per hint used
- Persistence: browser localStorage via streamlit-js-eval (per-browser, no auth)

## Exercise data structure
```
data/
├── index.yaml              # ordered list of exercise refs
├── exercises/*.yaml        # one file per exercise (nested schema)
└── solutions/*.py          # correct code (kept separate from YAML)
```

**`data/index.yaml`** format:
```yaml
exercises:
  - ref: var_rpg_001
  - ref: var_hack_001
  ...
```

**`data/exercises/{ref}.yaml`** schema:
```yaml
id: var_rpg_001
metadata:
  chapter: 1
  concept: variables
  subconcept: assignment
  difficulty: beginner
  theme: rpg              # used for display
  prerequisites: []       # exercise IDs that should come first
  tags: [variables, assignment]
content:
  prompt: |               # shown to the student
  initial_code: |         # starting code with bug
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

**`data/solutions/{ref}.py`** — pure Python, just the correct code. Not embedded in YAML to keep exercises distributable without answers.

## Adding a new exercise
1. Create `data/exercises/{unique_id}.yaml` with the schema above
2. Create `data/solutions/{unique_id}.py` with the correct code
3. Register it in `data/index.yaml` at the desired position
4. Run `pytest` to validate YAML integrity and solution correctness

## Chapters
- Ch 1: Variables (5 exercises — assignment, strings, floats, hex, boss)
- Ch 2: Control Flow (5 exercises — if/else, if/elif/else, nested if, comparison ops, boss)
- Ch 3: Functions (5 exercises — def/return, parameters, multiple params, defaults, boss)

## CI/CD
- GitHub Actions: `.github/workflows/ci.yml`
- Runs on push/PR to main: ruff, black --check, mypy, pytest --cov

## Gotchas
- `app/engine.py` uses `exec()` for code execution — no sandbox beyond isolated namespace
- Streamlit Cloud deploys from `main` using `requirements.txt` (not `requirements-dev.txt`)
- localStorage persistence is per-browser; no cross-device sync
- streamlit-code-editor returns a dict (`response["text"]`), not a plain string
- Live demo: https://hebikatagit-a96zsajn6ln94t2xfnxpcm.streamlit.app/

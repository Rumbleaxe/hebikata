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

## Code quality (no project config — tool defaults)
- Format: `black .`
- Lint: `ruff check .`
- Typecheck: `mypy .`

## Architecture
- Entrypoint: `app/main.py` — single Streamlit page with inline CSS (arcade green-terminal theme)
- Execution engine: `execute_code_with_tests()` at `app/main.py:64` — uses `exec()` in isolated namespace, runs all `test_*` functions found
- Session state tracked via `st.session_state` (successes, attempts, score, lives)
- Mastery = 3 successful completions per exercise, 50 points each, 3 lives total

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
pep_tip: "..."
boss: false               # true for boss-challenge exercises
```

**`data/solutions/{ref}.py`** — pure Python, just the correct code. Not embedded in YAML to keep exercises distributable without answers.

## Adding a new exercise
1. Create `data/exercises/{unique_id}.yaml` with the schema above
2. Create `data/solutions/{unique_id}.py` with the correct code
3. Register it in `data/index.yaml` at the desired position
4. Run `pytest` to validate YAML integrity and solution correctness

## Research notes
- `research/` — store findings on pedagogy, exercise design patterns, and effectiveness data
- `research/pedagogy/` — spaced repetition, mastery learning references
- `research/exercises/` — exercise design templates and schemas
- `research/results/` — user study data and analysis

## Gotchas
- No `pyproject.toml`, CI/CD, or tool-specific config exists yet
- Sphinx docs scaffold in `docs/` is skeleton (not populated)
- `app/main.py` uses `exec()` for code execution — no sandbox beyond isolated namespace
- Streamlit Cloud deploys from `main` using `requirements.txt` (not `requirements-dev.txt`)
- Live demo: https://hebikatagit-a96zsajn6ln94t2xfnxpcm.streamlit.app/

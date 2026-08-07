# AGENTS.md — hebikata

## Quick start
- Setup: `uv venv && uv pip install -r requirements-dev.txt`
- Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate`
- Run: `streamlit run app/main.py` (or `.\run_hebikata.bat` on Windows)
- Open: http://localhost:8501

## Commands
- `pytest` — runs all tests in `tests/`
- `pytest --cov` — with coverage
- `black .` — format
- `ruff check .` — lint
- `mypy app/` — typecheck (CI runs `mypy .` with `continue-on-error: true`, so mypy won't block PRs)
- All tool configs in `pyproject.toml`; Python >=3.12 required

## Architecture

| File | Purpose |
|------|---------|
| `app/main.py` | Entrypoint — injects parent dir into `sys.path`, sets page config, calls `render_app()` |
| `app/engine.py` | `execute_code_with_tests()` — `exec()` user code + test functions in isolated namespace |
| `app/data_loader.py` | `load_exercises()` — reads `data/index.yaml` + per-exercise YAMLs |
| `app/session.py` | Session state, localStorage persistence, navigation, hint system |
| `app/ui.py` | All Streamlit UI — purple dark theme, JetBrains Mono font, `streamlit-code-editor` |
| `tests/conftest.py` | Fixtures: `exercise_refs`, `exercises`, `exercise_dict`, `solutions` |
| `tests/test_session.py` | Tests for session state, navigation, hint system, persistence |

- Mastery = 3 successful completions per exercise, 50 points each, 3 lives total
- Hints: 3 levels (basic → detailed → solution), -10 points per hint
- Persistence: browser `localStorage` via `streamlit-js-eval` (per-browser, no auth, no cross-device sync)

## Exercise data

```
data/
├── index.yaml              # ordered list of exercise refs
├── exercises/{ref}.yaml    # one YAML per exercise: id, metadata, content, validation, hints, pep_tip, boss
└── solutions/{ref}.py      # plain Python — correct answer kept separate from YAML
```

Each YAML has: `id`, `metadata` (chapter, concept, subconcept, difficulty, theme, prerequisites, tags), `content` (prompt, initial_code), `validation` (tests as inline string), `hints` (3 levels with text), `pep_tip`, `boss` (bool).

Chapters: 1-Variables, 2-Control Flow, 3-Functions. 5 exercises each (4 themed + 1 boss).

## Adding an exercise
1. Create `data/exercises/{unique_id}.yaml` following the schema
2. Create `data/solutions/{unique_id}.py` with the correct code
3. Register in `data/index.yaml` at the desired position
4. Run `pytest` — validates YAML integrity and solution correctness

## Gotchas
- **`exec()` with no real sandbox** — `engine.py` uses `exec()` in an isolated namespace only. No RestrictedPython.
- **`streamlit-code-editor` returns a dict** — access code via `response["text"]`, detect submit via `response.get("type") == "submit"`.
- **Deploy uses `requirements.txt`, not `requirements-dev.txt`** — dev tools (black, ruff, mypy) excluded from Streamlit Cloud deploys.
- **`sys.path.insert(0, parent)` in `app/main.py`** — enables `from app.ui import render_app` without installing the package.
- **Prerequisites in YAML are validated by tests but NOT enforced at runtime** — the app doesn't block exercises out of order.
- **Boss exercises always use theme `arcade`**, not the chapter's theme.
- **Standard exercise ref naming**: `{chapter_abbrev}_{theme}_{seq}` (e.g., `ctrl_rpg_001`), where theme is `rpg|hack|sci|crypto`.
- **mypy fails don't block CI** — `continue-on-error: true` in the workflow.
- **Type hints use Python 3.12 style** — `dict` not `Dict`, `X | Y` not `Optional`, `list` not `List`.
- **CI runs ruff → black --check → mypy → pytest --cov** in that order on push/PR to main.

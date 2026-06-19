# Changelog

All notable changes to HebiKata will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-19

### Added

- **Chapter 2: Control Flow** — 5 new themed exercises:
  - RPG: if/else (warrior health check)
  - Hacking: if/elif/else (access level classifier)
  - Science: nested if (temperature phase classifier)
  - Crypto: comparison operators (hash difficulty validator)
  - Boss: review (game state machine)
- **Chapter 3: Functions** — 5 new themed exercises:
  - RPG: def + return (damage calculator)
  - Hacking: parameters (character decoder)
  - Science: multiple params (kinetic energy)
  - Crypto: default params (hash data function)
  - Boss: review (score calculator)
- **Session persistence** — progress saved to browser localStorage via streamlit-js-eval; survives refreshes and session timeouts
- **Code editor upgrade** — replaced `st.text_area` with `streamlit-code-editor` (syntax highlighting, dark theme, VSCode shortcuts, built-in Run button)
- **Progressive hint system** — 3 hint levels per exercise (basic → detailed → solution); each hint costs 10 points
- **Visual redesign** — purple dark theme (#a855f7 accent), Inter + JetBrains Mono fonts, rounded corners, gradient dividers, glow effects, pill-shaped stat badges, chapter-grouped progress panel with colored dots, boss badges
- **Modular architecture** — broke up 513-line `main.py` into:
  - `app/main.py` — slim entry point
  - `app/engine.py` — code execution engine
  - `app/data_loader.py` — YAML exercise loader
  - `app/session.py` — session state, persistence, navigation, hints
  - `app/ui.py` — all Streamlit UI and CSS
- **`pyproject.toml`** — centralized project metadata and tool configs (black, ruff, mypy, pytest)
- **CI/CD pipeline** — GitHub Actions workflow (`.github/workflows/ci.yml`) running ruff, black --check, mypy, pytest --cov on push/PR
- "Reset All Progress" button in sidebar

### Changed

- Existing Chapter 1 exercises retrofitted with 3-level hints (was single hint)
- `requirements.txt` updated: added `streamlit-code-editor`, `streamlit-js-eval`
- `requirements-dev.txt` updated: relaxed version pins to `>=` ranges
- Exercise count grew from 5 to 15 (3 chapters × 5 exercises each)
- Page layout changed to `initial_sidebar_state="collapsed"`
- All type annotations updated to Python 3.12 style (`dict` over `Dict`, `X | Y` over `Optional`)

### Removed

- Monolithic `app/main.py` (replaced by modular architecture)

## [0.1.0] - 2026-02-02

### Added

- Initial MVP release of HebiKata Python learning platform
- Core Streamlit application with arcade-themed UI (green terminal aesthetic)
- 5 themed exercises for Chapter 1 (Variables):
  - RPG: Wizard mana assignment
  - Hacking: Decrypt key strings
  - Science: Scientific notation floats
  - Crypto: Hexadecimal literals
  - Boss: Multiple variable challenge
- Live code execution with pytest-based validation
- Progress tracking system (3 successes to master each exercise)
- Lives and scoring system
- Hints and PEP8 tips for each exercise
- Exercise data structure in YAML format
- Split-screen layout: exercises on left, progress panel on right
- Navigation between exercises
- Error feedback with detailed messages
- Virtual environment setup with uv
- Test suite for core logic validation
- Documentation:
  - MVP_README.md with quick start guide
  - Updated .github/copilot-instructions.md
  - run_hebikata.bat launcher script
- Project structure:
  - app/ directory for application code
  - data/ directory for exercise definitions
  - .venv/ virtual environment

### Fixed

- Streamlit Cloud deployment: Removed Windows-only dependencies (pywin32)
- Created minimal requirements.txt for cross-platform deployment
- Added requirements-dev.txt for local development with all tools

### Infrastructure

- Python 3.12+ support
- Minimal dependencies for deployment: Streamlit 1.45.1, pytest 8.3.5, PyYAML
- Virtual environment management with uv
- Git repository initialization

## [Unreleased]

### Planned

- Auto-run tests on keystroke (real-time validation)
- Snake animation/visualization (visual feedback)
- 8-bit sound effects (audio engagement)
- Timer and keystroke tracking for scoring (performance metrics)
- Additional exercise chapters (4-10):
  - Data Structures
  - Strings/Files
  - Error Handling
  - OOP
  - Advanced Python
  - Libraries (NumPy/Pandas)
  - CS Fundamentals
- Leaderboard/achievement system
- Anti-cheat mechanisms
- LLM exercise generation
- Multiplayer/co-op mode

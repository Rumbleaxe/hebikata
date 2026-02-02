# Changelog

All notable changes to HebiKata will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Auto-run tests on keystroke
- Snake animation/visualization
- 8-bit sound effects
- Timer and keystroke tracking for scoring
- Session persistence (save progress to JSON)
- Better code editor integration (streamlit-ace)
- Additional exercise chapters (2-10):
  - Control Flow
  - Functions
  - Data Structures
  - Strings/Files
  - Error Handling
  - OOP
  - Advanced Python
  - Libraries (NumPy/Pandas)
  - CS Fundamentals
- Leaderboard system
- Anti-cheat mechanisms
- LLM exercise generation
- Multiplayer/co-op mode

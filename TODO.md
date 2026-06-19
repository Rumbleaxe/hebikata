# TODO

## 1. Create File/Folder Structure ✅ COMPLETE
- [x] Set up a new project directory
  - [x] Create the following folders:
    - `app/` - For core application code ✅
    - `data/` - For storing data files ✅
    - `docs/` - For documentation ✅
    - `scripts/` - For utility scripts (future)
  - [x] Initialize a `README.md` file ✅
  - [x] Add a `.gitignore` file to exclude unnecessary files ✅

## 2. Create MVP (Minimum Viable Product) ✅ COMPLETE
- [x] Develop core functionality
  - [x] Implement main features in `app/` directory
    - [x] main.py with Streamlit UI ✅
    - [x] Live code execution with pytest validation ✅
    - [x] Progress tracking (3 success system) ✅
    - [x] Lives and scoring system ✅
  - [x] Create exercise data structure
    - [x] exercises.yaml with 5 themed exercises ✅
  - [x] Ensure the application runs locally ✅
  - [x] Write basic tests for core functionality
    - [x] test_logic.py validates execution ✅
  - [x] Document the MVP features
    - [x] MVP_README.md with usage guide ✅

## 3. v0.2.0 Enhancements ✅ COMPLETE
**Status**: ✅ Complete
**Completed**: June 2026

- [x] Session persistence (localStorage via streamlit-js-eval)
- [x] Better code editor integration (streamlit-code-editor)
- [x] More exercise chapters (3 chapters, 15 exercises total)
  - [x] Chapter 2: Control Flow (if/else, if/elif/else, nested if, comparison ops, boss)
  - [x] Chapter 3: Functions (def/return, parameters, multiple params, defaults, boss)
- [x] Progressive hint system (3 levels per exercise, -10 points per hint)
- [x] Visual redesign (purple dark theme, JetBrains Mono, rounded corners, glow effects)
- [x] Modular architecture (broke up main.py into engine, data_loader, session, ui)
- [x] pyproject.toml (centralized project metadata and tool configs)
- [x] CI/CD pipeline (GitHub Actions: ruff, black, mypy, pytest)

## 4. Upload to Streamlit Host ✅ COMPLETE
- [x] Set up a Streamlit account
- [x] Deploy the application to Streamlit sharing platform
  - [x] Ensure all dependencies are listed in `requirements.txt` ✅
  - [x] Fix cross-platform compatibility (removed Windows-only packages) ✅
  - [x] Test the application on Streamlit Cloud ✅
  - [x] App live at: https://hebikatagit-a96zsajn6ln94t2xfnxpcm.streamlit.app/
- [x] Share the link with stakeholders for feedback ✅
- [ ] Consider custom domain setup (optional - future consideration)

## 5. Future Enhancements
**Status**: 📋 Planned
**Last Updated**: June 2026

- [ ] Auto-run tests on keystroke (real-time validation)
- [ ] Snake animation/visualization (visual feedback)
- [ ] 8-bit sound effects (audio engagement)
- [ ] Timer and keystroke tracking for scoring (performance metrics)
- [ ] Additional exercise chapters (4-10):
  - [ ] Data Structures
  - [ ] Strings/Files
  - [ ] Error Handling
  - [ ] OOP
  - [ ] Advanced Python
  - [ ] Libraries (NumPy/Pandas)
  - [ ] CS Fundamentals
- [ ] User analytics and learning progress tracking
- [ ] Leaderboard/achievement system
- [ ] Anti-cheat mechanisms
- [ ] Mobile responsive improvements

## 6. Maintenance & Operations
**Status**: ✅ Active

Ongoing tasks:
- [x] Monitor Streamlit Cloud app performance and uptime
- [x] Respond to user feedback and bug reports
- [ ] Periodically update dependencies (quarterly review)
- [ ] Add new Python exercises as requested by users
- [ ] Track analytics on exercise completion rates

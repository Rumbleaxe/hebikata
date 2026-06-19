# hebikata

[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-Interactive%20UI-orange)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Live App](https://img.shields.io/badge/live%20app-Streamlit%20Cloud-FF4B4B)](https://hebikatagit-a96zsajn6ln94t2xfnxpcm.streamlit.app/)

---

## 🚀 Try It Now!

**Live Demo:** [https://hebikatagit-a96zsajn6ln94t2xfnxpcm.streamlit.app/](https://hebikatagit-a96zsajn6ln94t2xfnxpcm.streamlit.app/)

Start learning Python through repetition immediately - no installation required!

---

## What is hebikata?

**hebikata** is a self-hosted, interactive Python e-learning platform inspired by the disciplined repetition of *karate kata* and modern textbook pedagogy.
It helps students master Python programming through scaffolded, incremental exercises repeated with varied inputs — reinforcing correct coding principles by practice and feedback.

---

## Key Features

- 🖥️ **Live Python Editor:** Syntax-highlighted code editor with real-time pytest validation
- 🔄 **Repetition-Based Learning:** Each exercise requires 3 successes with immediate feedback for mastery
- 📚 **15 Themed Exercises:** 3 chapters × 5 exercises (RPG, Hacking, Science, Crypto, Boss per chapter)
- ✅ **Automated Testing:** Immediate correctness feedback with pytest-based validation
- 🎯 **Progressive Difficulty:** Exercises increase in complexity, reinforcing fundamentals and best practices
- 💜 **Modern Dark Theme:** Purple accent design with JetBrains Mono font and smooth animations
- 💡 **Progressive Hints:** 3-level hint system (basic → detailed → solution) with score penalty
- 💾 **Session Persistence:** Progress auto-saved to browser localStorage
- 🏗️ **Modular Architecture:** Clean separation of engine, UI, session, and data loading

---

## Current Status: v0.2.0

✅ **Chapter 1: Variables** — 5 exercises covering:
- Variable assignment
- String literals
- Scientific notation (floats)
- Hexadecimal literals
- Multiple variable challenges (boss)

✅ **Chapter 2: Control Flow** — 5 exercises covering:
- if/else conditions
- if/elif/else branching
- Nested conditions
- Comparison operators
- Game state machine (boss)

✅ **Chapter 3: Functions** — 5 exercises covering:
- def and return
- Function parameters
- Multiple parameters
- Default parameters
- Score calculator (boss)

🚧 **Coming Soon:**
- Additional chapters (Data Structures, Strings/Files, Error Handling, OOP, etc.)
- Snake animation visualizations
- 8-bit sound effects
- Auto-run tests on keystroke

---

## Why hebikata?

- **Spaced Repetition & Mastery:** Repetition with variation boosts retention and deep understanding
- **Project-Based & Modular:** Exercises framed as real-world problems, chunked into manageable lessons
- **Immediate Feedback:** Automated tests and hints catch errors early, accelerating learning
- **Clean Code Focus:** Enforces PEP 8 and Pythonic idioms for writing maintainable, professional code
- **Self-Hosted & Extensible:** Full control over learning environment, easy to customize and extend

---

## Getting Started (Local Development)

### 1. Clone the repo

```bash
git clone https://github.com/Rumbleaxe/hebikata.git
cd hebikata
```

### 2. Set up environment

```bash
# Create virtual environment with uv
uv venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Unix/macOS:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements-dev.txt
```

### 3. Run locally

```bash
# Windows (quick launcher)
.\run_hebikata.bat

# Or manually
streamlit run app\main.py
```

### 4. Start learning

Open http://localhost:8501 in your browser and start mastering Python!

---

## Project Structure

```
hebikata/
├── app/                        # Core Streamlit application
│   ├── main.py                # Entry point — page config + render_app() call
│   ├── engine.py              # execute_code_with_tests() — exec() in isolated namespace
│   ├── data_loader.py         # load_exercises() — reads index.yaml + per-file YAMLs
│   ├── session.py             # Session state, persistence (localStorage), navigation, hints
│   └── ui.py                  # All Streamlit UI, CSS theme, code editor, layout
├── data/
│   ├── index.yaml             # Ordered list of exercise refs
│   ├── exercises/*.yaml       # One file per exercise (nested schema)
│   └── solutions/*.py         # Correct code (kept separate from YAML)
├── tests/
│   ├── conftest.py            # Fixtures for loading exercises/solutions
│   ├── test_execution_engine.py   # Validates execute_code_with_tests()
│   ├── test_exercise_data.py      # Validates all exercise YAMLs
│   └── test_exercise_solutions.py # Auto-validates solutions pass their tests
├── .github/
│   ├── copilot-instructions.md     # AI assistant guidance
│   └── workflows/ci.yml            # CI: ruff, black, mypy, pytest
├── pyproject.toml              # Project metadata + tool configs
├── requirements.txt           # Minimal deployment dependencies
├── requirements-dev.txt       # Full development dependencies
└── run_hebikata.bat           # Windows quick launcher
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting issues and pull requests, coding standards, and testing requirements.

---

## Documentation

- **Architecture:** [AGENTS.md](AGENTS.md) — detailed architecture, exercise schema, and development guide
- **Changes:** [CHANGELOG.md](CHANGELOG.md) — Version history and updates

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

---

## Acknowledgments

Inspired by the disciplined practice of karate kata and modern Python best practices, combining repetition, immediate feedback, and project-based learning to create a unique, effective Python education platform.

---

<div align="center">
<sub>Made with ❤️ for Python learners and educators</sub>
</div>

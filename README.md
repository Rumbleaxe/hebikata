# hebikata

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
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

- 🖥️ **Live Python Editor:** Interactive code editor with real-time pytest validation  
- 🔄 **Repetition-Based Learning:** Each exercise requires 3 successes with immediate feedback for mastery  
- 📚 **Themed Variety:** 5 contextually varied exercises (RPG, Hacking, Science, Crypto, Boss Challenge)  
- ✅ **Automated Testing:** Immediate correctness feedback with pytest-based validation  
- 🎯 **Progressive Difficulty:** Exercises increase in complexity, reinforcing fundamentals and best practices  
- 🎮 **Arcade Aesthetic:** 8-bit inspired green terminal theme for immersive learning experience
- 💡 **Hints & Tips:** Built-in help system with PEP8 style guidance

---

## Current Status: MVP (v0.1.0)

✅ **Chapter 1: Variables** - 5 exercises covering:
- Variable assignment
- String literals
- Scientific notation (floats)
- Hexadecimal literals
- Multiple variable challenges

🚧 **Coming Soon:**
- Additional chapters (Control Flow, Functions, Data Structures, etc.)
- Snake animation visualizations
- 8-bit sound effects
- Auto-run tests on keystroke
- Session persistence and progress saving

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
├── app/                    # Core Streamlit application
│   └── main.py            # Main app with UI and execution logic
├── data/                   # Exercise definitions
│   └── exercises.yaml     # 5 themed exercises for Chapter 1
├── docs/                   # Sphinx documentation
├── .github/               # GitHub configuration
│   └── copilot-instructions.md  # AI assistant guidance
├── requirements.txt       # Minimal deployment dependencies
├── requirements-dev.txt   # Full development dependencies
├── test_logic.py         # Core logic validation tests
├── run_hebikata.bat      # Windows quick launcher
└── MVP_README.md         # Detailed MVP documentation
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting issues and pull requests, coding standards, and testing requirements.

---

## Documentation

- **Quick Start:** [MVP_README.md](MVP_README.md) - Detailed usage guide and feature overview
- **Development:** [.github/copilot-instructions.md](.github/copilot-instructions.md) - Architecture and conventions
- **Changes:** [CHANGELOG.md](CHANGELOG.md) - Version history and updates

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

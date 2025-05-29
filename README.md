# hebikata

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-Interactive%20UI-orange)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

---

## What is hebikata?

**hebikata** is a self-hosted, interactive Python e-learning platform inspired by the disciplined repetition of *karate kata* and modern textbook pedagogy.  
It helps students master Python programming through scaffolded, incremental exercises repeated with varied inputs — reinforcing correct coding principles by practice and feedback.

---

## Key Features

- 🖥️ **Live Python Editor:** Large, interactive terminal window for coding directly in the browser  
- 🔄 **Repetition-Based Learning:** Each exercise repeated 5 times with different variations for mastery  
- 📚 **Structured Curriculum:** Chapters → Sections → Exercises → Variations (5×5×5 matrix)  
- ✅ **Automated Testing:** Immediate correctness feedback with pytest-based validation  
- 🎯 **Progressive Difficulty:** Exercises increase in complexity, reinforcing fundamentals and best practices  
- 🛠️ **Code Quality Tools:** Integrated linting and formatting guidance (ruff, black, mypy)  

---

## Why hebikata?

- **Spaced Repetition & Mastery:** Repetition with variation boosts retention and deep understanding  
- **Project-Based & Modular:** Exercises framed as real-world problems, chunked into manageable lessons  
- **Immediate Feedback:** Automated tests and hints catch errors early, accelerating learning  
- **Clean Code Focus:** Enforces PEP 8 and Pythonic idioms for writing maintainable, professional code  
- **Self-Hosted & Extensible:** Full control over learning environment, easy to customize and extend  

---

## Getting Started

1. **Clone the repo:**  
```

git clone https://github.com/your-org/hebikata.git
cd hebikata

```

2. **Install dependencies:**  
```

pip install -r requirements.txt

```

3. **Run the app:**  
```

streamlit run app/main.py

```

4. **Start learning:**  
Open the browser window, follow the interactive exercises, and watch your Python skills grow!

---

## Project Structure

- `app/` — Core Streamlit app code, UI components, exercises, and tests  
- `data/` — Exercise input variations and hints (JSON files)  
- `docs/` — Curriculum design and pedagogical notes  
- `scripts/` — Dev and deployment helpers  
- `requirements.txt` — Python dependencies  
- `LICENSE` — Apache 2.0 license  

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting issues and pull requests, coding standards, and testing requirements.

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

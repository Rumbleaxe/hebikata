# HebiKata - Quick Start Guide

## What You Have

A full-featured Python learning platform with:

- ✅ 15 themed exercises across 3 chapters (Variables, Control Flow, Functions)
- ✅ Syntax-highlighted code editor with VSCode shortcuts
- ✅ Session persistence (progress saved to browser localStorage)
- ✅ Progressive hint system (3 levels per exercise)
- ✅ Purple dark theme with JetBrains Mono font
- ✅ Live code execution with pytest validation
- ✅ Progress tracking (3 successes to master each exercise)
- ✅ Lives/Score system
- ✅ PEP8 tips
- ✅ Chapter-grouped navigation

## Running the App

### 1. Activate Virtual Environment

```bash
# Windows
.\.venv\Scripts\activate

# Unix/macOS
source .venv/bin/activate
```

### 2. Launch the App

```bash
streamlit run app\main.py
```

The app will open in your browser at http://localhost:8501

### 3. Using the App

1. **Read the exercise prompt** — each has a fun theme (wizard, hacker, scientist, etc.)
2. **Edit the code** in the syntax-highlighted editor to fix the bug
3. **Click "🧪 Run Tests"** (or the Play button in the editor) to validate your solution
4. **Success**: Get +50 points, progress counter increases
5. **Failure**: Lose a life, see error message with details
6. **Master the kata**: Get 3 successes to complete each exercise
7. **Use hints**: Click "💡 Show Hint" to reveal progressive hints (costs 10 points each)
8. **Navigate**: Use Previous/Next buttons to move between exercises
9. **Progress is saved**: Your score, lives, and mastery state persist across browser sessions

## Architecture

```
app/
├── main.py         # Entry point — page config + render_app() call
├── engine.py       # execute_code_with_tests() — exec() in isolated namespace
├── data_loader.py  # load_exercises() — reads index.yaml + per-file YAMLs
├── session.py      # Session state, persistence (localStorage), navigation, hints
└── ui.py           # All Streamlit UI, CSS theme, code editor, layout
```

## Adding New Exercises

1. Create `data/exercises/{unique_id}.yaml` with the schema:
   ```yaml
   id: ctrl_rpg_001
   metadata:
     chapter: 2
     concept: control-flow
     subconcept: if-else
     difficulty: beginner
     theme: rpg
     prerequisites: [var_boss_001]
     tags: [control-flow, if, else]
   content:
     prompt: |
       Your exercise description here
     initial_code: |
       # Starting code with bug
   validation:
     tests: |
       def test_something():
           assert condition, "Error message"
   hints:
     - level: basic
       text: "Gentle nudge"
     - level: detailed
       text: "More specific hint"
     - level: solution
       text: "The answer"
   pep_tip: "Style guidance"
   boss: false
   ```

2. Create `data/solutions/{unique_id}.py` with the correct code
3. Register it in `data/index.yaml` at the desired position
4. Run `pytest` to validate YAML integrity and solution correctness

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov

# Code quality
ruff check .
black --check .
mypy app/
```

## Known Limitations

- No auto-run (must click "Run Tests" or Play button)
- No snake animation (just text-based progress)
- No sound effects
- No timer/keystroke tracking
- No cross-device sync (localStorage is per-browser)
- `exec()` has no sandbox beyond isolated namespace

---

🐍 **Happy Coding! Master Python through repetition!** 🐍

# HebiKata MVP - Quick Start Guide

## What You Have

A functional MVP of the HebiKata Python learning platform with:

- ✅ 5 themed exercises (RPG, Hacking, Science, Crypto, Boss)
- ✅ Live code execution with pytest validation
- ✅ Arcade-themed UI with green terminal aesthetic
- ✅ Progress tracking (3 successes to master each exercise)
- ✅ Lives/Score system
- ✅ Hints and PEP8 tips
- ✅ Navigation between exercises

## Running the MVP

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

1. **Read the exercise prompt** - Each has a fun theme (wizard, hacker, etc.)
2. **Edit the code** in the text area to fix the bug
3. **Click "🧪 Run Tests"** to validate your solution
4. **Success**: Get +50 points, progress counter increases
5. **Failure**: Lose a life, see error message
6. **Master the kata**: Get 3 successes to complete each exercise
7. **Use hints**: Click "💡 Show Hint" if stuck

## File Structure

```
hebikata/
├── app/
│   └── main.py              # Main Streamlit application
├── data/
│   └── exercises.yaml       # 5 exercise definitions
├── .venv/                   # Virtual environment (created)
├── test_logic.py            # Logic validation tests
└── requirements.txt         # Dependencies
```

## Next Steps for Enhancement

### Priority Features (from design docs)

1. **Auto-run on keystroke**: Execute tests automatically as user types
2. **Snake animation**: Visual feedback (segments destroyed on success, snake grows on failure)
3. **Sound effects**: 8-bit beeps for correct answers
4. **Timer**: Track time per exercise for scoring
5. **Keystroke tracking**: Count keystrokes for optimal solution scoring
6. **More exercises**: Add Chapters 2-10 (control flow, functions, etc.)

### Quick Enhancements

1. **Better code editor**: Replace `st.text_area` with `st.code_editor` (streamlit-ace)
2. **Session persistence**: Save progress to JSON file
3. **Leaderboard**: Track high scores across sessions
4. **Dark mode polish**: Add CRT scanline effects, better color scheme

## Testing

Run the logic tests:

```bash
python test_logic.py
```

All 4 tests should pass:
- ✅ Successful code execution
- ✅ Failed assertion detection
- ✅ Syntax error handling
- ✅ String variable testing

## Known Limitations

- No auto-run (must click "Run Tests" button)
- No actual snake animation (just text-based progress)
- No sound effects
- No timer/keystroke tracking
- Fixed set of 5 exercises (no dynamic loading)
- No session persistence (progress resets on refresh)

## Adding New Exercises

Edit `data/exercises.yaml` and add a new entry:

```yaml
  - id: your_exercise_id
    level: beginner
    concept: variables
    theme: yourtheme
    prompt: |
      Your exercise description here
    initial_code: |
      # Starting code with bug
    pytest_tests: |
      def test_something():
          assert condition, "Error message"
    hint: "Help text"
    pep_tip: "Style guidance"
```

## Troubleshooting

**Import Error**: Make sure you're in the virtual environment:
```bash
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix
```

**YAML Error**: Check indentation in `data/exercises.yaml` (use 2 spaces)

**Streamlit Not Found**: Install dependencies:
```bash
uv pip install pyyaml streamlit pytest
```

---

🐍 **Happy Coding! Master Python through repetition!** 🐍

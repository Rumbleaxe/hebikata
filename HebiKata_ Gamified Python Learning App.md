<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# HebiKata: Gamified Python Learning App

HebiKata (Japanese for "Snake Kata") is an open-source, Streamlit-based web app that teaches Python through continuously evaluating REPL exercises in an authentic 8-bit arcade environment, using pytest for robust code validation and spaced repetition for mastery.

## Core Learning Philosophy

Combines Rustlings-style broken code fixes with VimTutor interactivity, spaced repetition (SRS), interleaved practice across themed variants (RPG wizards, hacking challenges, scientific puzzles), and progressive CS curriculum matching ideal Python ToC. Muscle memory builds through 3-5 contextually varied repetitions per concept before advancement.

## Tech Stack

- **Frontend/Backend**: Streamlit with real-time `st.code` REPL + `streamlit_exec`
- **Testing**: pytest for comprehensive exercise validation
- **License**: MIT (GitHub-hosted, Streamlit Cloud deployment)
- **Exercise Format**: YAML (structured, extensible):

```yaml
id: var_wizard_001
level: beginner
concept: variables
theme: rpg
prompt: "Set wizard's mana to 100"
initial_code: "mana = 50  # Fix me!"
pytest_tests: |
  def test_mana():
      assert mana == 100, "Mana must be 100"
hint: "Use = for assignment (mana = value)"
pep_tip: "PEP8: snake_case (player_mana)"
srs_interval: 3  # Days before retry
```


## Key Features

### 1. Live Evaluating REPL

- **Split Screen**: Left = exercise + editable code box (actively runs on every keystroke/change)
- **pytest Validation**: Real-time test execution with pass/fail feedback
- **Dual Modes**: Fix broken code (80%) or write from scratch (20%)
- **Auto-advance**: 3/5 successes unlocks next variant


### 2. Authentic 8-Bit Arcade Interface

- **Right Panel**: Snake-inspired invaders descend (nod to Japanese arcade roots)
    - Correct answer = snake segment destroyed (+score, arcade "beep!")
    - Wrong answer = snake grows longer (lose life)
    - **Future**: Authentic coin-op graphics/sounds (Space Invaders-style urgency)
- **Visual Design**: 8-bit pixel art, CRT scanlines, neon glow (large 32px monospace fonts)
- **Lives/Score**: 3 lives, combo multipliers for streaks


### 3. Spaced Repetition \& Themed Variety

**SRS Algorithm**: Expanding intervals (1d→3d→7d→14d), interleaving 5 themed variants:

1. **RPG**: `wizard_mana = 100`
2. **Hacking**: `decrypt_key = "skRM9x"`
3. **Science**: `neutron_mass = 1.675e-27`
4. **Puzzle**: `portal_charge = 7`
5. **Crypto**: `nonce = 0xdeadbeef`

### 4. Progressive Curriculum (10 Chapters)

1. Setup/Variables | 2. Control Flow | 3. Functions | 4. Data Structures
2. Strings/Files | 6. Errors/Debug | 7. OOP | 8. Advanced Python
3. Libraries (NumPy/Pandas) | 10. CS Fundamentals (Algorithms/DBs)

### 5. Support \& Standards

- **Live Hints**: Tooltip explains principle + minimal working example
- **PEP8 Linter**: Real-time flake8 integration with fix suggestions
- **Debug Mode**: Step-through execution visualization


### 6. Accessible UI/UX

- **Massive Typography**: 28px+ monospace (IBM Plex Mono)
- **High Contrast**: Black/\#00FF41 (matrix green) on CRT-style background
- **Mobile-first**: Collapsible panels, touch-optimized


## Future Roadmap

### Phase 2: Anti-Cheat \& Skill Scoring

```
Score = (Keystrokes Efficiency × Speed Bonus × Attempts Penalty × Streak Multiplier)
- Time: <2min = 100%, >5min = 50%
- Keystrokes: Optimal path = 100%, copy-paste = 0%
- Attempts: 1st try = 100%, 3+ tries = 50%
```

**Anti-cheat**: Disable paste (JS monitor), detect code similarity, keyboard event tracking

### Phase 3: LLM Exercise Generation

- GPT-based exercise creator from YAML templates
- Infinite themed variants: "Generate 5 variable exercises as cyberpunk hacker missions"


### Phase 4: Immersive Arcade Experience

- **8-bit Assets**: Authentic Space Invaders/Pac-Man sprites + chiptune SFX
- **Coin-Op UX**: "Insert Coin" animations, cabinet lighting effects


### Phase 5: HebiKata Network (Cybersecurity RPG)

```
"Hack into the HebiKata underground server network.
Your mentor: ShadowSnake, legendary Python ninja.
Mission: Infiltrate corporate databases using ethical SQL injection.
Tools: Your Python REPL + real SQLite/NoSQL playground."
```

- Roleplay missions teaching cybersecurity (SQL injection, XSS prevention, encryption)
- "Hackable" Streamlit app with easter eggs and secret levels
- Multiplayer co-op coding challenges


## App Flow

```
Home → Chapter Select → Snake Arena Loads
1. Read themed prompt (2min)
2. Fix/write code in live REPL (pytest runs continuously)
3. Snake reacts instantly (destroy segment = +50pts)
4. Hint/PEP8 if stuck → 3/5 successes → Next variant
5. Chapter complete → Boss alien (10 themed questions)
```


## Creator Workflow

```
hebi-exercises/
├── beginner/
│   ├── variables/
│   │   ├── wizard.yaml
│   │   ├── hacker.yaml
│   │   └── science.yaml
└── advanced/
    └── algorithms/big_o.yaml
```


## Success Metrics

- **Retention**: 85% SRS completion after 30 days
- **Engagement**: Average 45min sessions (arcade addiction factor)
- **Skill**: 90% pass rate on pytest suite after 3 exposures

HebiKata transforms Python learning into an addictive 8-bit karate dojo where muscle memory meets spaced repetition, delivering Space Invaders urgency with Rustlings rigor and cybersecurity intrigue. Deployable today, infinitely expandable.


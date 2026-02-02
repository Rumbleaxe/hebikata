<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# HebiKata: First Exercise Set (Chapter 1 - Setup \& Basics)

**Research Basis**: Optimal sessions = **25-40 minutes**. Per exercise: **2-4 minutes effort** max to maintain flow state/interest. **5 exercises per concept** with themed variety prevents boredom while building muscle memory via spaced repetition. Total set = **~30min session**.[^2][^5][^7]

## Session Design

```
Total Time: 30 minutes (5 exercises × 4min + 2min breaks + 3min boss)
Per Exercise: Read (30s) → Code (2min) → Test (30s) → Snake reacts (30s)
Break: 2min between exercises (Snake mini-game or stretch)
```


## YAML Exercise Set: Variables (5 Variants)

### 1. RPG Wizard (2.5min expected)

```yaml
id: var_rpg_001
level: beginner
concept: variables
theme: rpg
prompt: |
  🧙‍♂️ Your wizard casts Fireball! Set mana to 100.
initial_code: |
  mana = 50  # Too low for Fireball!
pytest_tests: |
  def test_mana():
      assert mana == 100, "Fireball needs 100 mana!"
hint: "Use = to assign: mana = 100"
pep_tip: "PEP8: snake_case (player_mana), not camelCase"
srs_interval: 1
score_factors: {time: 100, attempts: 100, keystrokes: 8}
```


### 2. Hacker Terminal (2min expected)

```yaml
id: var_hack_001  
level: beginner
concept: variables
theme: hacking
prompt: |
  💀 Terminal> Set decrypt_key to access mainframe
initial_code: |
  decrypt_key = "guest"  # Wrong credentials
pytest_tests: |
  def test_key():
      assert decrypt_key == "skRM9x", "Access denied"
hint: "decrypt_key = 'skRM9x' (quotes for strings)"
pep_tip: "String literals use single or double quotes"
srs_interval: 1
```


### 3. Science Lab (3min expected - introduces float)

```yaml
id: var_sci_001
level: beginner
concept: variables-numbers
theme: science
prompt: |
  🧪 Neutron mass = 1.675e-27 kg. Set it correctly.
initial_code: |
  neutron_mass = 1.675  # Missing scientific notation
pytest_tests: |
  def test_neutron():
      assert abs(neutron_mass - 1.675e-27) < 1e-28
hint: "Use e for scientific notation: 1.675e-27"
pep_tip: "Floats for decimals, meaningful names"
```


### 4. Crypto Puzzle (2min expected)

```yaml
id: var_crypto_001
level: beginner
concept: variables-hex
theme: crypto
prompt: |
  🔐 Nonce must be 0xdeadbeef for blockchain validation
initial_code: |
  nonce = 3735928559  # Decimal form - convert!
pytest_tests: |
  def test_nonce():
      assert hex(nonce) == "0xdeadbeef"
hint: "nonce = 0xdeadbeef (0x prefix for hex)"
pep_tip: "Hex literals start with 0x"
```


### 5. BOSS: Mixed Challenge (4min expected)

```yaml
id: var_boss_001
level: beginner
concept: variables-review
theme: arcade
prompt: |
  🎮 HIGH SCORE! Set all 3 variables correctly:
  * player_lives = 3
  * score = 0 
  * high_score = 999999
initial_code: |
  player_lives = 1
  score = 100
  high_score = 1000  # Beat the arcade record!
pytest_tests: |
  def test_arcade():
      assert player_lives == 3
      assert score == 0  
      assert high_score == 999999
hint: "Fix all 3 assignments above"
pep_tip: "Consistency: all snake_case, same style"
snake_boss: true  # Triggers special animation
```


## Live REPL Behavior (Streamlit)

```
1. Code box auto-runs pytest on every keystroke
2. Green: ✅ Tests pass → Snake segment explodes (50pts + beep!)
3. Red: ❌ Tests fail → Snake grows (lose 1/3 lives)
4. 3/5 successes → "Kata Complete!" → Next exercise
5. Boss kill → Chapter unlock + 500pt bonus
```


## Pacing \& Flow Control

```
Exercise 1 (2:30) → 2min break (Snake dodges)  
Exercise 2 (2:00) → 2min break
Exercise 3 (3:00) → 2min break  
Exercise 4 (2:00) → 2min break
BOSS (4:00) → Chapter Complete (1min celebration)

TOTAL: 28 minutes optimal flow
```


## Score Algorithm (Future Anti-Cheat Ready)

```
Base: 100pts × (1.0 - attempts/10) × (2min/time_taken) × (optimal_keystrokes/actual)
Example: 1st try, 90s, 8 keystrokes = 100 × 1.0 × 1.33 × 1.0 = 133pts
Copy-paste detected = 0pts
```

This set hits **research-optimal 25-40min** with **2-4min micro-sessions**, 8-bit urgency via live feedback, and 5x themed variety for spaced repetition - transforming variable assignment into an addictive Snake kata dojo.
<span style="display:none">[^1][^10][^3][^4][^6][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://pubmed.ncbi.nlm.nih.gov/24500777/

[^2]: https://automated-training.com/how-long-should-be-a-training-session/

[^3]: https://accellier.edu.au/live-online-learning-duration/

[^4]: https://files.eric.ed.gov/fulltext/EJ1304918.pdf

[^5]: https://simplyelearning.com.au/optimal-learning-time-before-switch-off/

[^6]: https://www.reddit.com/r/Anki/comments/jcne2p/what_research_has_been_done_for_a_rough_optimal/

[^7]: https://hub.jhu.edu/2017/12/18/how-long-to-break-practice-to-improve-learning/

[^8]: https://www.reddit.com/r/askscience/comments/qdj46t/is_there_a_scientific_consensus_on_optimal/

[^9]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5126970/

[^10]: https://www.learningscientists.org/blog/2018/7/5-1


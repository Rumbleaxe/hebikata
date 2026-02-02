"""
HebiKata - Python Learning Through Repetition

Main Streamlit application entry point. This module implements an interactive
Python learning platform that uses spaced repetition and themed exercises to
teach programming fundamentals.

The application provides:
- Live code execution with pytest validation
- Progress tracking (3 successes to master each exercise)
- Arcade-themed UI with hints and PEP8 tips
- Navigation between themed exercises

Architecture:
    - Exercises are defined in YAML format (data/exercises.yaml)
    - Each exercise contains: prompt, initial code, pytest tests, hints
    - Session state tracks user progress across exercises
    - Code execution happens in isolated namespaces for safety

Author: HebiKata Contributors
License: Apache 2.0
"""

import streamlit as st
import yaml
from pathlib import Path
from typing import Dict, List, Any
import traceback

# Configure Streamlit page settings before any other st commands
# This must be the first Streamlit command in the app
st.set_page_config(
    page_title="HebiKata - Python Kata Dojo",
    page_icon="🐍",
    layout="wide",  # Use full width for split-screen layout
    initial_sidebar_state="expanded"
)


def load_exercises() -> List[Dict[str, Any]]:
    """
    Load exercises from YAML file.
    
    Reads the exercises.yaml file from the data directory and parses it into
    a list of exercise dictionaries. Each exercise contains metadata like
    ID, theme, prompt, code, tests, and hints.
    
    Returns:
        List[Dict[str, Any]]: List of exercise dictionaries with keys:
            - id: Unique exercise identifier
            - level: Difficulty level (e.g., "beginner")
            - concept: Programming concept being taught
            - theme: Exercise theme (rpg, hacking, science, etc.)
            - prompt: Exercise instructions for the user
            - initial_code: Starting code with bugs to fix
            - pytest_tests: Test function code to validate solution
            - hint: Help text for stuck users
            - pep_tip: PEP8 style guidance
            
    Raises:
        FileNotFoundError: If exercises.yaml doesn't exist
        yaml.YAMLError: If YAML file is malformed
    """
    exercises_path = Path(__file__).parent.parent / "data" / "exercises.yaml"
    with open(exercises_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data['exercises']


def execute_code_with_tests(user_code: str, test_code: str) -> Dict[str, Any]:
    """
    Execute user code and run pytest tests against it.
    
    This function safely executes user-provided Python code in an isolated
    namespace, then runs pytest test functions against it to validate the
    solution. Both code and tests execute in the same namespace to allow
    tests to access user-defined variables.
    
    Security Note:
        Uses exec() in isolated namespace. In production, consider additional
        sandboxing (e.g., RestrictedPython) for untrusted user input.
    
    Args:
        user_code: The user's Python code to execute and test
        test_code: The pytest test function code (must define function
                   starting with 'test_')
        
    Returns:
        Dict[str, Any]: Result dictionary with keys:
            - success (bool): True if all tests passed, False otherwise
            - message (str): User-friendly success/failure message
            - error (str or None): Detailed error traceback if failed, None if success
            
    Examples:
        >>> result = execute_code_with_tests(
        ...     "mana = 100",
        ...     "def test_mana():\\n    assert mana == 100"
        ... )
        >>> result['success']
        True
        
        >>> result = execute_code_with_tests(
        ...     "mana = 50",
        ...     "def test_mana():\\n    assert mana == 100"
        ... )
        >>> result['success']
        False
    """
    # Create an isolated namespace for code execution
    # This prevents user code from accessing or modifying app state
    namespace = {}
    
    try:
        # Execute user code first to populate namespace with variables
        exec(user_code, namespace)
        
        # Execute test code in same namespace so tests can access user variables
        exec(test_code, namespace)
        
        # Find the test function in the namespace
        # pytest convention: test functions start with 'test_'
        test_func = None
        for name, obj in namespace.items():
            if name.startswith('test_') and callable(obj):
                test_func = obj
                break
        
        # Validate that we found a test function
        if test_func is None:
            return {
                'success': False,
                'message': 'No test function found',
                'error': 'Test code must define a function starting with test_'
            }
        
        # Run the test function - will raise AssertionError if test fails
        test_func()
        
        # If we get here, all tests passed
        return {
            'success': True,
            'message': '✅ All tests passed!',
            'error': None
        }
        
    except AssertionError as e:
        # Test assertion failed - user code doesn't meet requirements
        return {
            'success': False,
            'message': f'❌ Test failed: {str(e)}',
            'error': str(e)
        }
    except Exception as e:
        # Syntax error, runtime error, or other exception in user code
        return {
            'success': False,
            'message': f'❌ Error: {type(e).__name__}',
            'error': traceback.format_exc()
        }


def initialize_session_state():
    """
    Initialize Streamlit session state variables.
    
    Session state persists data across reruns of the Streamlit app.
    This function sets up all necessary state variables on first run,
    including exercise data, progress tracking, and user scores.
    
    Session State Variables:
        exercises (List[Dict]): All loaded exercises from YAML
        current_exercise_idx (int): Index of currently active exercise
        user_code (str): Current code in the editor
        successes (List[int]): Success count for each exercise (need 3 to master)
        attempts (List[int]): Total attempts for each exercise
        score (int): Total score across all exercises
        lives (int): Remaining lives (lose 1 per failed attempt)
        
    Note:
        Only initializes variables that don't exist. Safe to call multiple times.
    """
    # Load exercises from YAML file on first run
    if 'exercises' not in st.session_state:
        st.session_state.exercises = load_exercises()
    
    # Start at first exercise
    if 'current_exercise_idx' not in st.session_state:
        st.session_state.current_exercise_idx = 0
    
    # Initialize code editor with current exercise's starting code
    if 'user_code' not in st.session_state:
        current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
        st.session_state.user_code = current_exercise['initial_code']
    
    # Track successes for each exercise (need 3 to master)
    if 'successes' not in st.session_state:
        st.session_state.successes = [0] * len(st.session_state.exercises)
    
    # Track total attempts for each exercise (for statistics)
    if 'attempts' not in st.session_state:
        st.session_state.attempts = [0] * len(st.session_state.exercises)
    
    # Initialize score (gain 50 points per success)
    if 'score' not in st.session_state:
        st.session_state.score = 0
    
    # Initialize lives (lose 1 per failure, start with 3)
    if 'lives' not in st.session_state:
        st.session_state.lives = 3


def reset_exercise_code():
    """
    Reset code editor to initial state for current exercise.
    
    Useful when user wants to start over or undo their changes.
    Loads the initial_code from the current exercise and updates
    the session state.
    
    Side Effects:
        Modifies st.session_state.user_code
    """
    current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
    st.session_state.user_code = current_exercise['initial_code']


def next_exercise():
    """
    Navigate to next exercise in the sequence.
    
    Increments the current exercise index and loads the initial code
    for the new exercise. Does nothing if already at the last exercise.
    
    Side Effects:
        Modifies st.session_state.current_exercise_idx
        Modifies st.session_state.user_code
    """
    # Check if there's a next exercise available
    if st.session_state.current_exercise_idx < len(st.session_state.exercises) - 1:
        st.session_state.current_exercise_idx += 1
        # Load initial code for new exercise
        current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
        st.session_state.user_code = current_exercise['initial_code']


def previous_exercise():
    """
    Navigate to previous exercise in the sequence.
    
    Decrements the current exercise index and loads the initial code
    for the previous exercise. Does nothing if already at the first exercise.
    
    Side Effects:
        Modifies st.session_state.current_exercise_idx
        Modifies st.session_state.user_code
    """
    # Check if there's a previous exercise available
    if st.session_state.current_exercise_idx > 0:
        st.session_state.current_exercise_idx -= 1
        # Load initial code for previous exercise
        current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
        st.session_state.user_code = current_exercise['initial_code']


def main():
    """
    Main application entry point.
    
    This function orchestrates the entire HebiKata user interface:
    1. Initializes session state
    2. Applies custom CSS for arcade theme
    3. Renders header with stats (lives, score, progress)
    4. Creates split-screen layout:
       - Left: Exercise prompt and code editor
       - Right: Progress panel and navigation
    5. Handles user interactions (run tests, reset, hints, navigation)
    
    The UI is organized as:
        Header (title + stats bar)
        ├── Left Column (2/3 width)
        │   ├── Exercise prompt
        │   ├── Code editor (text area)
        │   └── Action buttons (Run, Reset, Hint)
        └── Right Column (1/3 width)
            ├── Progress tracker
            ├── PEP8 tip
            └── Navigation buttons
    
    Note:
        This function is called on every Streamlit rerun (button click, etc.)
    """
    # Initialize all session state variables
    initialize_session_state()
    
    # Apply custom CSS for 8-bit arcade aesthetic
    # Matrix green (#00FF41) on black background with monospace fonts
    st.markdown("""
        <style>
        /* Global app background */
        .stApp {
            background-color: #000000;
        }
        /* Main title styling */
        .main-title {
            color: #00FF41;
            font-family: 'Courier New', monospace;
            font-size: 48px;
            text-align: center;
            text-shadow: 0 0 10px #00FF41;
            margin-bottom: 20px;
        }
        /* Exercise title styling */
        .exercise-title {
            color: #00FF41;
            font-family: 'Courier New', monospace;
            font-size: 28px;
            margin-bottom: 10px;
        }
        /* Exercise prompt box */
        .prompt-text {
            color: #FFFFFF;
            font-family: 'Courier New', monospace;
            font-size: 20px;
            background-color: #1a1a1a;
            padding: 20px;
            border-radius: 5px;
            border: 2px solid #00FF41;
        }
        /* Stats bar text */
        .stats-text {
            color: #00FF41;
            font-family: 'Courier New', monospace;
            font-size: 18px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # === HEADER SECTION ===
    # Display main title and tagline
    st.markdown('<div class="main-title">🐍 HEBIKATA 🐍</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #00FF41; font-family: monospace; font-size: 18px; margin-bottom: 30px;">PYTHON KATA DOJO - Master through repetition</div>', unsafe_allow_html=True)
    
    # === STATS BAR ===
    # Display lives, score, current exercise number, and progress
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stats-text">❤️ Lives: {st.session_state.lives}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stats-text">🎯 Score: {st.session_state.score}</div>', unsafe_allow_html=True)
    with col3:
        current_idx = st.session_state.current_exercise_idx
        st.markdown(f'<div class="stats-text">📚 Exercise: {current_idx + 1}/{len(st.session_state.exercises)}</div>', unsafe_allow_html=True)
    with col4:
        successes = st.session_state.successes[current_idx]
        st.markdown(f'<div class="stats-text">✅ Progress: {successes}/3</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === MAIN CONTENT AREA ===
    # Get the current exercise data
    current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
    
    # Create split-screen layout: 2/3 for exercise, 1/3 for progress panel
    left_col, right_col = st.columns([2, 1])
    
    # === LEFT COLUMN: Exercise and Code Editor ===
    with left_col:
        # Display exercise title and prompt
        st.markdown(f'<div class="exercise-title">Exercise {current_idx + 1}: {current_exercise["theme"].upper()}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="prompt-text">{current_exercise["prompt"]}</div>', unsafe_allow_html=True)
        
        st.markdown("### Your Code:")
        
        # Code editor (text area that syncs with session state)
        user_code = st.text_area(
            "Code",
            value=st.session_state.user_code,
            height=200,
            key="code_editor",
            label_visibility="collapsed"  # Hide the "Code" label
        )
        # Update session state with any code changes
        st.session_state.user_code = user_code
        
        # === ACTION BUTTONS ===
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        
        # RUN TESTS BUTTON
        with btn_col1:
            if st.button("🧪 Run Tests", use_container_width=True, type="primary"):
                # Increment attempt counter for statistics
                st.session_state.attempts[current_idx] += 1
                
                # Execute user code and run pytest tests
                result = execute_code_with_tests(
                    st.session_state.user_code,
                    current_exercise['pytest_tests']
                )
                
                if result['success']:
                    # SUCCESS: Increment success counter and award points
                    st.session_state.successes[current_idx] += 1
                    st.session_state.score += 50
                    st.success(result['message'])
                    
                    # Check if exercise is mastered (3 successful attempts)
                    if st.session_state.successes[current_idx] >= 3:
                        st.balloons()  # Celebration animation
                        st.success("🎉 Exercise Complete! You've mastered this kata!")
                else:
                    # FAILURE: Lose a life and show error message
                    st.session_state.lives -= 1
                    st.error(result['message'])
                    
                    # Show detailed error traceback if available
                    if result['error']:
                        with st.expander("Show Error Details"):
                            st.code(result['error'])
        
        # RESET BUTTON
        with btn_col2:
            if st.button("🔄 Reset Code", use_container_width=True):
                reset_exercise_code()
                st.rerun()  # Force Streamlit to rerun and refresh UI
        
        # HINT BUTTON
        with btn_col3:
            if st.button("💡 Show Hint", use_container_width=True):
                st.info(f"**Hint:** {current_exercise['hint']}")
    
    # === RIGHT COLUMN: Progress Panel ===
    with right_col:
        st.markdown("### 📊 Progress")
        
        # Display progress for all exercises with visual indicators
        for idx, exercise in enumerate(st.session_state.exercises):
            success_count = st.session_state.successes[idx]
            attempt_count = st.session_state.attempts[idx]
            is_current = idx == st.session_state.current_exercise_idx
            
            # Visual status indicator
            # 🟢 = Mastered (3+ successes)
            # 🟡 = In Progress (1-2 successes)
            # ⚪ = Not Started (0 successes)
            status = "🟢" if success_count >= 3 else "🟡" if success_count > 0 else "⚪"
            current_marker = "👉 " if is_current else ""  # Arrow for current exercise
            
            st.markdown(f"{current_marker}{status} **{exercise['theme'].title()}** - {success_count}/3 successes ({attempt_count} attempts)")
        
        st.markdown("---")
        
        # Display PEP8 style tip for current exercise
        st.markdown("### 💡 PEP8 Tip")
        st.info(current_exercise.get('pep_tip', 'Keep your code clean and readable!'))
        
        st.markdown("---")
        
        # === NAVIGATION CONTROLS ===
        st.markdown("### 🎮 Navigation")
        # Previous/Next navigation buttons
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            # Disable if at first exercise
            if st.button("⬅️ Previous", disabled=current_idx == 0, use_container_width=True):
                previous_exercise()
                st.rerun()
        with nav_col2:
            # Disable if at last exercise
            if st.button("Next ➡️", disabled=current_idx == len(st.session_state.exercises) - 1, use_container_width=True):
                next_exercise()
                st.rerun()
    
    # === FOOTER ===
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #00FF41; font-family: monospace; font-size: 14px;">'
        'Practice makes perfect. 3 successes unlock mastery. 🐍'
        '</div>',
        unsafe_allow_html=True
    )


# Entry point - runs when script is executed directly
if __name__ == "__main__":
    main()

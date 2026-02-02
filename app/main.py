"""
HebiKata - Python Learning Through Repetition
Main Streamlit application entry point.
"""

import streamlit as st
import yaml
from pathlib import Path
from typing import Dict, List, Any
import io
import sys
import traceback

# Page configuration
st.set_page_config(
    page_title="HebiKata - Python Kata Dojo",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_exercises() -> List[Dict[str, Any]]:
    """Load exercises from YAML file."""
    exercises_path = Path(__file__).parent.parent / "data" / "exercises.yaml"
    with open(exercises_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data['exercises']


def execute_code_with_tests(user_code: str, test_code: str) -> Dict[str, Any]:
    """
    Execute user code and run pytest tests against it.
    
    Args:
        user_code: The user's Python code
        test_code: The pytest test function code
        
    Returns:
        Dict with keys: success (bool), message (str), error (str or None)
    """
    # Create a namespace for execution
    namespace = {}
    
    try:
        # Execute user code
        exec(user_code, namespace)
        
        # Execute test code in same namespace
        exec(test_code, namespace)
        
        # Find and run the test function
        test_func = None
        for name, obj in namespace.items():
            if name.startswith('test_') and callable(obj):
                test_func = obj
                break
        
        if test_func is None:
            return {
                'success': False,
                'message': 'No test function found',
                'error': 'Test code must define a function starting with test_'
            }
        
        # Run the test
        test_func()
        
        return {
            'success': True,
            'message': '✅ All tests passed!',
            'error': None
        }
        
    except AssertionError as e:
        return {
            'success': False,
            'message': f'❌ Test failed: {str(e)}',
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'❌ Error: {type(e).__name__}',
            'error': traceback.format_exc()
        }


def initialize_session_state():
    """Initialize session state variables."""
    if 'exercises' not in st.session_state:
        st.session_state.exercises = load_exercises()
    
    if 'current_exercise_idx' not in st.session_state:
        st.session_state.current_exercise_idx = 0
    
    if 'user_code' not in st.session_state:
        current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
        st.session_state.user_code = current_exercise['initial_code']
    
    if 'successes' not in st.session_state:
        st.session_state.successes = [0] * len(st.session_state.exercises)
    
    if 'attempts' not in st.session_state:
        st.session_state.attempts = [0] * len(st.session_state.exercises)
    
    if 'score' not in st.session_state:
        st.session_state.score = 0
    
    if 'lives' not in st.session_state:
        st.session_state.lives = 3


def reset_exercise_code():
    """Reset code to initial state for current exercise."""
    current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
    st.session_state.user_code = current_exercise['initial_code']


def next_exercise():
    """Move to next exercise."""
    if st.session_state.current_exercise_idx < len(st.session_state.exercises) - 1:
        st.session_state.current_exercise_idx += 1
        current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
        st.session_state.user_code = current_exercise['initial_code']


def previous_exercise():
    """Move to previous exercise."""
    if st.session_state.current_exercise_idx > 0:
        st.session_state.current_exercise_idx -= 1
        current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
        st.session_state.user_code = current_exercise['initial_code']


def main():
    """Main application function."""
    initialize_session_state()
    
    # Custom CSS for arcade theme
    st.markdown("""
        <style>
        .stApp {
            background-color: #000000;
        }
        .main-title {
            color: #00FF41;
            font-family: 'Courier New', monospace;
            font-size: 48px;
            text-align: center;
            text-shadow: 0 0 10px #00FF41;
            margin-bottom: 20px;
        }
        .exercise-title {
            color: #00FF41;
            font-family: 'Courier New', monospace;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .prompt-text {
            color: #FFFFFF;
            font-family: 'Courier New', monospace;
            font-size: 20px;
            background-color: #1a1a1a;
            padding: 20px;
            border-radius: 5px;
            border: 2px solid #00FF41;
        }
        .stats-text {
            color: #00FF41;
            font-family: 'Courier New', monospace;
            font-size: 18px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-title">🐍 HEBIKATA 🐍</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #00FF41; font-family: monospace; font-size: 18px; margin-bottom: 30px;">PYTHON KATA DOJO - Master through repetition</div>', unsafe_allow_html=True)
    
    # Stats bar
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
    
    # Get current exercise
    current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
    
    # Split screen layout
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # Exercise prompt
        st.markdown(f'<div class="exercise-title">Exercise {current_idx + 1}: {current_exercise["theme"].upper()}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="prompt-text">{current_exercise["prompt"]}</div>', unsafe_allow_html=True)
        
        st.markdown("### Your Code:")
        
        # Code editor
        user_code = st.text_area(
            "Code",
            value=st.session_state.user_code,
            height=200,
            key="code_editor",
            label_visibility="collapsed"
        )
        st.session_state.user_code = user_code
        
        # Action buttons
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        
        with btn_col1:
            if st.button("🧪 Run Tests", use_container_width=True, type="primary"):
                st.session_state.attempts[current_idx] += 1
                result = execute_code_with_tests(
                    st.session_state.user_code,
                    current_exercise['pytest_tests']
                )
                
                if result['success']:
                    st.session_state.successes[current_idx] += 1
                    st.session_state.score += 50
                    st.success(result['message'])
                    
                    # Check if exercise is complete (3 successes)
                    if st.session_state.successes[current_idx] >= 3:
                        st.balloons()
                        st.success("🎉 Exercise Complete! You've mastered this kata!")
                else:
                    st.session_state.lives -= 1
                    st.error(result['message'])
                    if result['error']:
                        with st.expander("Show Error Details"):
                            st.code(result['error'])
        
        with btn_col2:
            if st.button("🔄 Reset Code", use_container_width=True):
                reset_exercise_code()
                st.rerun()
        
        with btn_col3:
            if st.button("💡 Show Hint", use_container_width=True):
                st.info(f"**Hint:** {current_exercise['hint']}")
    
    with right_col:
        # Progress and help panel
        st.markdown("### 📊 Progress")
        
        # Show progress for all exercises
        for idx, exercise in enumerate(st.session_state.exercises):
            success_count = st.session_state.successes[idx]
            attempt_count = st.session_state.attempts[idx]
            is_current = idx == st.session_state.current_exercise_idx
            
            status = "🟢" if success_count >= 3 else "🟡" if success_count > 0 else "⚪"
            current_marker = "👉 " if is_current else ""
            
            st.markdown(f"{current_marker}{status} **{exercise['theme'].title()}** - {success_count}/3 successes ({attempt_count} attempts)")
        
        st.markdown("---")
        
        st.markdown("### 💡 PEP8 Tip")
        st.info(current_exercise.get('pep_tip', 'Keep your code clean and readable!'))
        
        st.markdown("---")
        
        st.markdown("### 🎮 Navigation")
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("⬅️ Previous", disabled=current_idx == 0, use_container_width=True):
                previous_exercise()
                st.rerun()
        with nav_col2:
            if st.button("Next ➡️", disabled=current_idx == len(st.session_state.exercises) - 1, use_container_width=True):
                next_exercise()
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #00FF41; font-family: monospace; font-size: 14px;">'
        'Practice makes perfect. 3 successes unlock mastery. 🐍'
        '</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

"""
HebiKata - Session State & Persistence Management

Manages Streamlit session state for user progress tracking and provides
localStorage-based persistence via streamlit-js-eval so progress survives
browser refreshes and session timeouts.
"""

import json
from typing import Any

import streamlit as st
from streamlit_js_eval import get_local_storage, set_local_storage

from app.data_loader import load_exercises

STORAGE_KEY = "hebikata_progress"

DEFAULT_LIVES = 3
MASTERY_THRESHOLD = 3
POINTS_PER_SUCCESS = 50
HINT_PENALTY = 10


def save_progress() -> None:
    """Serialize current session state to browser localStorage."""
    state = {
        "successes": st.session_state.successes,
        "attempts": st.session_state.attempts,
        "score": st.session_state.score,
        "lives": st.session_state.lives,
        "current_exercise_idx": st.session_state.current_exercise_idx,
        "hint_levels": st.session_state.hint_levels,
    }
    set_local_storage(STORAGE_KEY, json.dumps(state))


def load_progress() -> dict[str, Any] | None:
    """Deserialize saved progress from browser localStorage."""
    raw = get_local_storage(STORAGE_KEY)
    if raw:
        try:
            return json.loads(raw)  # type: ignore[no-any-return]
        except (json.JSONDecodeError, TypeError):
            return None
    return None


def reset_all_progress() -> None:
    """Clear localStorage and reset all session state variables."""
    set_local_storage(STORAGE_KEY, "")
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def initialize_session_state() -> None:
    """
    Initialize Streamlit session state variables.

    On first run, attempts to restore progress from localStorage.
    Falls back to defaults if no saved data exists or if the exercise
    count has changed (e.g., after an update adding new exercises).
    """
    if "exercises" not in st.session_state:
        st.session_state.exercises = load_exercises()

    num_exercises = len(st.session_state.exercises)

    if "successes" not in st.session_state:
        saved = load_progress()
        if saved and len(saved.get("successes", [])) == num_exercises:
            st.session_state.successes = saved["successes"]
            st.session_state.attempts = saved["attempts"]
            st.session_state.score = saved["score"]
            st.session_state.lives = saved["lives"]
            st.session_state.current_exercise_idx = saved["current_exercise_idx"]
            st.session_state.hint_levels = saved.get(
                "hint_levels", [-1] * num_exercises
            )
        else:
            st.session_state.successes = [0] * num_exercises
            st.session_state.attempts = [0] * num_exercises
            st.session_state.score = 0
            st.session_state.lives = DEFAULT_LIVES
            st.session_state.current_exercise_idx = 0
            st.session_state.hint_levels = [-1] * num_exercises

    if "user_code" not in st.session_state:
        current_exercise = st.session_state.exercises[
            st.session_state.current_exercise_idx
        ]
        st.session_state.user_code = current_exercise["content"]["initial_code"]


def reset_exercise_code() -> None:
    """Reset code editor to initial state for current exercise."""
    current_exercise = st.session_state.exercises[st.session_state.current_exercise_idx]
    st.session_state.user_code = current_exercise["content"]["initial_code"]


def next_exercise() -> None:
    """Navigate to next exercise in the sequence."""
    if st.session_state.current_exercise_idx < len(st.session_state.exercises) - 1:
        st.session_state.current_exercise_idx += 1
        current_exercise = st.session_state.exercises[
            st.session_state.current_exercise_idx
        ]
        st.session_state.user_code = current_exercise["content"]["initial_code"]


def previous_exercise() -> None:
    """Navigate to previous exercise in the sequence."""
    if st.session_state.current_exercise_idx > 0:
        st.session_state.current_exercise_idx -= 1
        current_exercise = st.session_state.exercises[
            st.session_state.current_exercise_idx
        ]
        st.session_state.user_code = current_exercise["content"]["initial_code"]


def get_current_exercise() -> dict[str, Any]:
    """Return the currently active exercise dictionary."""
    return st.session_state.exercises[st.session_state.current_exercise_idx]  # type: ignore[no-any-return]


def get_current_hint_level() -> int:
    """Return the hint level for the current exercise (-1 = no hint shown)."""
    return st.session_state.hint_levels[st.session_state.current_exercise_idx]  # type: ignore[no-any-return]


def advance_hint() -> str | None:
    """
    Advance to the next hint level for the current exercise.

    Returns the hint text to display, or None if no more hints available.
    Deducts HINT_PENALTY points from the score for each hint used.
    """
    current_exercise = get_current_exercise()
    hints = current_exercise.get("hints", [])
    current_level = get_current_hint_level()
    next_level = current_level + 1

    if next_level >= len(hints):
        return None

    st.session_state.hint_levels[st.session_state.current_exercise_idx] = next_level
    st.session_state.score = max(0, st.session_state.score - HINT_PENALTY)
    save_progress()
    return hints[next_level]["text"]  # type: ignore[no-any-return]

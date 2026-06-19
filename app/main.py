"""
HebiKata - Python Learning Through Repetition

Main Streamlit application entry point.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.ui import render_app

st.set_page_config(
    page_title="HebiKata - Python Kata Dojo",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

render_app()

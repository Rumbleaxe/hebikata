"""
HebiKata - Python Learning Through Repetition

Main Streamlit application entry point.
"""

import streamlit as st

from app.ui import render_app

st.set_page_config(
    page_title="HebiKata - Python Kata Dojo",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if __name__ == "__main__":
    render_app()

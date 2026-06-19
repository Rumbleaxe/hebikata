"""
HebiKata - UI Rendering

All Streamlit UI code including the arcade-themed visual design,
exercise display, code editor, progress panel, and navigation.
"""

import streamlit as st
from code_editor import code_editor

from app.engine import execute_code_with_tests
from app.session import (
    MASTERY_THRESHOLD,
    POINTS_PER_SUCCESS,
    advance_hint,
    get_current_exercise,
    get_current_hint_level,
    initialize_session_state,
    next_exercise,
    previous_exercise,
    reset_all_progress,
    reset_exercise_code,
    save_progress,
)

THEME = {
    "bg": "#0f0f1a",
    "surface": "#1e1b2e",
    "border": "#2d2b3d",
    "accent": "#a855f7",
    "accent_light": "#c084fc",
    "accent_glow": "rgba(168, 85, 247, 0.3)",
    "text": "#e2e8f0",
    "text_muted": "#94a3b8",
    "success": "#34d399",
    "error": "#f87171",
    "warning": "#fbbf24",
}

THEME_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

.stApp {{
    background-color: {THEME["bg"]};
}}

/* Hide default Streamlit header */
header[data-testid="stHeader"] {{
    background-color: {THEME["bg"]} !important;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: {THEME["surface"]} !important;
    border-right: 1px solid {THEME["border"]} !important;
}}

/* Main title */
.main-title {{
    font-family: 'Inter', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(135deg, {THEME["accent"]}, {THEME["accent_light"]});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}}

.main-subtitle {{
    text-align: center;
    color: {THEME["text_muted"]};
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    margin-bottom: 1.5rem;
    font-weight: 400;
}}

/* Stat pills */
.stat-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    font-weight: 500;
    color: {THEME["text"]};
    background-color: {THEME["surface"]};
    border: 1px solid {THEME["border"]};
}}

.stat-pill .label {{
    color: {THEME["text_muted"]};
    font-weight: 400;
}}

/* Cards */
.hk-card {{
    background-color: {THEME["surface"]};
    border: 1px solid {THEME["border"]};
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s ease;
}}

.hk-card:hover {{
    box-shadow: 0 0 20px {THEME["accent_glow"]};
}}

/* Exercise prompt */
.prompt-box {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem;
    line-height: 1.7;
    color: {THEME["text"]};
    background-color: {THEME["surface"]};
    padding: 1.25rem;
    border-radius: 12px;
    border: 1px solid {THEME["border"]};
    border-left: 3px solid {THEME["accent"]};
}}

/* Section headings */
.section-title {{
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: {THEME["text"]};
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* Gradient divider */
.gradient-divider {{
    height: 2px;
    background: linear-gradient(90deg, {THEME["accent"]}, {THEME["accent_light"]}, transparent);
    border: none;
    margin: 1.25rem 0;
}}

/* Progress item */
.progress-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    border-radius: 8px;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: {THEME["text"]};
    margin-bottom: 4px;
    transition: background 0.15s ease;
}}

.progress-item:hover {{
    background-color: rgba(168, 85, 247, 0.08);
}}

.progress-item.current {{
    background-color: rgba(168, 85, 247, 0.12);
    border: 1px solid {THEME["accent"]};
}}

.progress-item .dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}}

.dot.mastered {{ background-color: {THEME["success"]}; box-shadow: 0 0 6px {THEME["success"]}; }}
.dot.in-progress {{ background-color: {THEME["warning"]}; box-shadow: 0 0 6px {THEME["warning"]}; }}
.dot.not-started {{ background-color: {THEME["border"]}; }}

/* PEP tip */
.pep-tip-box {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: {THEME["text_muted"]};
    background-color: rgba(168, 85, 247, 0.08);
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border-left: 3px solid {THEME["accent_light"]};
}}

/* Boss badge */
.boss-badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #fff;
    background: linear-gradient(135deg, {THEME["accent"]}, #ec4899);
    margin-left: 8px;
}}

/* Chapter badge */
.chapter-badge {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    color: {THEME["accent_light"]};
    background-color: rgba(168, 85, 247, 0.15);
    border: 1px solid {THEME["accent"]};
    margin-right: 8px;
}}

/* Hint box */
.hint-box {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    color: {THEME["warning"]};
    background-color: rgba(251, 191, 36, 0.08);
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border-left: 3px solid {THEME["warning"]};
}}

/* Footer */
.footer-text {{
    text-align: center;
    color: {THEME["text_muted"]};
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
}}

/* Override Streamlit buttons */
.stButton > button {{
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    border: 1px solid {THEME["border"]} !important;
    color: {THEME["text"]} !important;
    background-color: {THEME["surface"]} !important;
}}

.stButton > button:hover {{
    border-color: {THEME["accent"]} !important;
    box-shadow: 0 0 12px {THEME["accent_glow"]} !important;
    color: {THEME["accent_light"]} !important;
}}

.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {THEME["accent"]}, #7c3aed) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 0 20px {THEME["accent_glow"]} !important;
}}

.stButton > button[kind="primary"]:hover {{
    box-shadow: 0 0 25px rgba(168, 85, 247, 0.5) !important;
}}

/* Code editor container styling */
.element-container:has(.stCodeEditor),
.element-container:has(div[data-testid="stCodeEditor"]) {{
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid {THEME["border"]};
}}

/* Streamlit info/success/error boxes */
element-container:has(div[data-testid="stSuccess"]) {{
    border-radius: 8px;
}}

/* Override Streamlit text area if fallback */
.stTextArea > div > div > textarea {{
    background-color: {THEME["surface"]} !important;
    color: {THEME["text"]} !important;
    border: 1px solid {THEME["border"]} !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}}

/* Mastery celebration */
.mastery-text {{
    font-family: 'Inter', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: {THEME["success"]};
    text-align: center;
    padding: 0.5rem;
}}

/* Reset button */
.reset-btn {{
    color: {THEME["error"]} !important;
    font-size: 0.8rem !important;
}}
</style>
"""


def _render_header() -> None:
    st.markdown('<div class="main-title">HebiKata</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">Python Kata Dojo — Master through repetition</div>',
        unsafe_allow_html=True,
    )


def _render_stats_bar() -> None:
    current_idx = st.session_state.current_exercise_idx
    successes = st.session_state.successes[current_idx]
    total_exercises = len(st.session_state.exercises)

    cols = st.columns(4)
    stats = [
        ("❤️", "Lives", str(st.session_state.lives)),
        ("🎯", "Score", str(st.session_state.score)),
        ("📚", "Exercise", f"{current_idx + 1}/{total_exercises}"),
        ("✅", "Progress", f"{successes}/{MASTERY_THRESHOLD}"),
    ]
    for col, (icon, label, value) in zip(cols, stats, strict=False):
        with col:
            st.markdown(
                f'<div class="stat-pill">{icon} <span class="label">{label}:</span> {value}</div>',
                unsafe_allow_html=True,
            )


def _render_exercise_prompt() -> None:
    current_exercise = get_current_exercise()
    current_idx = st.session_state.current_exercise_idx
    is_boss = current_exercise.get("boss", False)
    chapter = current_exercise["metadata"]["chapter"]
    theme = current_exercise["metadata"]["theme"].upper()

    title_parts = f'<span class="chapter-badge">Ch {chapter}</span>'
    title_parts += f"Exercise {current_idx + 1}: {theme}"
    if is_boss:
        title_parts += '<span class="boss-badge">Boss</span>'

    st.markdown(
        f'<div class="section-title">{title_parts}</div>', unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="prompt-box">{current_exercise["content"]["prompt"]}</div>',
        unsafe_allow_html=True,
    )


def _render_code_editor() -> None:
    st.markdown('<div class="section-title">Your Code</div>', unsafe_allow_html=True)

    editor_buttons = [
        {
            "name": "Run",
            "feather": "Play",
            "primary": True,
            "hasText": True,
            "showWithIcon": True,
            "commands": ["submit"],
            "style": {"bottom": "0.4rem", "right": "0.4rem"},
        }
    ]

    response = code_editor(
        st.session_state.user_code,
        lang="python",
        theme="contrast",
        height=[8, 20],
        shortcuts="vscode",
        key="code_editor",
        buttons=editor_buttons,
        response_mode="debounce",
    )

    if response and response.get("text") is not None:
        st.session_state.user_code = response["text"]

    if response and response.get("type") == "submit":
        _run_tests()


def _run_tests() -> None:
    current_exercise = get_current_exercise()
    current_idx = st.session_state.current_exercise_idx

    st.session_state.attempts[current_idx] += 1

    result = execute_code_with_tests(
        st.session_state.user_code, current_exercise["validation"]["tests"]
    )

    if result["success"]:
        st.session_state.successes[current_idx] += 1
        st.session_state.score += POINTS_PER_SUCCESS
        st.success(result["message"])

        if st.session_state.successes[current_idx] >= MASTERY_THRESHOLD:
            st.balloons()
            st.markdown(
                '<div class="mastery-text">🎉 Exercise Complete! You\'ve mastered this kata!</div>',
                unsafe_allow_html=True,
            )
    else:
        st.session_state.lives -= 1
        st.error(result["message"])
        if result["error"]:
            with st.expander("Show Error Details"):
                st.code(result["error"])

    save_progress()


def _render_action_buttons() -> None:
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:
        if st.button("🧪 Run Tests", use_container_width=True, type="primary"):
            _run_tests()

    with btn_col2:
        if st.button("🔄 Reset Code", use_container_width=True):
            reset_exercise_code()
            st.rerun()

    with btn_col3:
        if st.button("💡 Show Hint", use_container_width=True):
            hint_text = advance_hint()
            if hint_text:
                current_level = get_current_hint_level()
                current_exercise = get_current_exercise()
                hints = current_exercise.get("hints", [])
                total_hints = len(hints)
                st.markdown(
                    f'<div class="hint-box">💡 Hint {current_level + 1}/{total_hints}: {hint_text}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.info("No more hints available for this exercise!")


def _render_progress_panel() -> None:
    st.markdown('<div class="section-title">📊 Progress</div>', unsafe_allow_html=True)

    current_chapter = None
    for idx, exercise in enumerate(st.session_state.exercises):
        chapter = exercise["metadata"]["chapter"]
        if chapter != current_chapter:
            current_chapter = chapter
            st.markdown(
                f'<div style="color: {THEME["accent_light"]}; font-family: Inter, sans-serif; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 0.5rem; margin-bottom: 0.25rem;">Chapter {chapter}</div>',
                unsafe_allow_html=True,
            )

        success_count = st.session_state.successes[idx]
        is_current = idx == st.session_state.current_exercise_idx

        dot_class = (
            "mastered"
            if success_count >= MASTERY_THRESHOLD
            else "in-progress" if success_count > 0 else "not-started"
        )
        current_class = " current" if is_current else ""
        theme_name = exercise["metadata"]["theme"].title()

        st.markdown(
            f'<div class="progress-item{current_class}">'
            f'<span class="dot {dot_class}"></span>'
            f"{'👉 ' if is_current else ''}"
            f"<strong>{theme_name}</strong> — {success_count}/{MASTERY_THRESHOLD}"
            f"</div>",
            unsafe_allow_html=True,
        )


def _render_pep_tip() -> None:
    current_exercise = get_current_exercise()
    tip = current_exercise.get("pep_tip", "Keep your code clean and readable!")
    st.markdown('<div class="section-title">💡 PEP8 Tip</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pep-tip-box">{tip}</div>', unsafe_allow_html=True)


def _render_navigation() -> None:
    current_idx = st.session_state.current_exercise_idx
    total = len(st.session_state.exercises)

    st.markdown(
        '<div class="section-title">🎮 Navigation</div>', unsafe_allow_html=True
    )
    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        if st.button("⬅️ Previous", disabled=current_idx == 0, use_container_width=True):
            previous_exercise()
            save_progress()
            st.rerun()

    with nav_col2:
        if st.button(
            "Next ➡️", disabled=current_idx == total - 1, use_container_width=True
        ):
            next_exercise()
            save_progress()
            st.rerun()


def _render_footer() -> None:
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="footer-text">Practice makes perfect. {MASTERY_THRESHOLD} successes unlock mastery. 🐍</div>',
        unsafe_allow_html=True,
    )


def render_app() -> None:
    """Main application render function — orchestrates all UI components."""
    initialize_session_state()
    st.markdown(THEME_CSS, unsafe_allow_html=True)

    _render_header()
    _render_stats_bar()
    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    left_col, right_col = st.columns([2, 1])

    with left_col:
        _render_exercise_prompt()
        _render_code_editor()
        _render_action_buttons()

    with right_col:
        _render_progress_panel()
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        _render_pep_tip()
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        _render_navigation()
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        if st.button("🗑️ Reset All Progress", use_container_width=True):
            reset_all_progress()

    _render_footer()

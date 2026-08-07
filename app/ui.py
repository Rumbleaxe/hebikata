"""
HebiKata - UI Rendering

Streamlit UI: brand-themed visual design, exercise display,
code editor, progress panel, navigation, and action buttons.
"""

from pathlib import Path

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

_CSS_PATH = Path(__file__).parent / "static" / "theme.css"


def _theme_css() -> str:
    if _CSS_PATH.is_file():
        return _CSS_PATH.read_text(encoding="utf-8")
    return ""


# ═══════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════


def _render_header() -> None:
    st.markdown(
        '<div class="main-logo">'
        '<span class="prompt">$</span><span class="name">hebikata</span>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="main-subtitle">Python Kata Dojo</div>',
        unsafe_allow_html=True,
    )


def _render_stats_bar() -> None:
    current_idx = st.session_state.current_exercise_idx
    successes = st.session_state.successes[current_idx]
    total = len(st.session_state.exercises)

    cells = [
        ("LIVES", str(st.session_state.lives)),
        ("SCORE", str(st.session_state.score)),
        ("EXERCISE", f"{current_idx + 1}/{total}"),
        ("PROGRESS", f"{successes}/{MASTERY_THRESHOLD}"),
    ]
    html = '<div class="stats-bar">'
    for label, value in cells:
        html += (
            f'<div class="stats-cell">'
            f'<span class="sig-value">{value}</span>'
            f'<span class="sig-label">{label}</span>'
            f"</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def _render_exercise_prompt() -> None:
    current_exercise = get_current_exercise()
    current_idx = st.session_state.current_exercise_idx
    is_boss = current_exercise.get("boss", False)
    chapter = current_exercise["metadata"]["chapter"]
    theme = current_exercise["metadata"]["theme"].upper()

    badges = f'<span class="chapter-badge">Ch {chapter}</span>'
    if is_boss:
        badges += '<span class="boss-badge">Boss</span>'

    st.markdown(
        f'<div class="section-title">{badges} {theme} &mdash; Exercise {current_idx + 1}</div>',
        unsafe_allow_html=True,
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
        key=f"code_editor_{st.session_state.current_exercise_idx}",
        buttons=editor_buttons,
        response_mode="debounce",
    )

    if response is not None and response.get("text") is not None:
        st.session_state.user_code = response["text"]

    if response is not None and response.get("type") == "submit":
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
    else:
        st.session_state.lives -= 1

    mastery = (
        result["success"]
        and st.session_state.successes[current_idx] >= MASTERY_THRESHOLD
    )

    st.session_state.last_result = {
        "success": result["success"],
        "message": result["message"],
        "error": result.get("error"),
        "mastery": mastery,
    }

    save_progress()


def _render_test_result() -> None:
    result = st.session_state.get("last_result")
    if result is None:
        return

    if result["success"]:
        st.success(result["message"])
        if result["mastery"]:
            st.balloons()
            st.markdown(
                '<div class="mastery-text">Exercise Complete — kata mastered!</div>',
                unsafe_allow_html=True,
            )
    else:
        st.error(result["message"])
        if result["error"]:
            with st.expander("Error Details"):
                st.code(result["error"])

    st.session_state.last_result = None


def _render_action_buttons() -> None:
    current_idx = st.session_state.current_exercise_idx
    total = len(st.session_state.exercises)

    nav1, nav2, act1, act2, act3 = st.columns([0.8, 0.8, 1.2, 1, 1])

    with nav1:
        st.button(
            "⬅ Prev",
            disabled=current_idx == 0,
            use_container_width=True,
            on_click=_navigate_previous,
        )

    with nav2:
        st.button(
            "Next ➡",
            disabled=current_idx == total - 1,
            use_container_width=True,
            on_click=_navigate_next,
        )

    with act1:
        st.button(
            "🧪 Run Tests",
            use_container_width=True,
            type="primary",
            on_click=_run_tests,
        )

    with act2:
        _render_hint_popover()

    with act3:
        st.button("🔄 Reset", use_container_width=True, on_click=reset_exercise_code)


def _render_hint_popover() -> None:
    current_idx = st.session_state.current_exercise_idx
    current_level = get_current_hint_level()
    hints = get_current_exercise().get("hints", [])

    with st.popover("💡 Hint", use_container_width=True):
        if current_level >= 0:
            shown_idx = min(current_level, len(hints) - 1)
            st.caption(f"Hint {shown_idx + 1}/{len(hints)}")
            st.markdown(
                f'<div class="hint-box">{hints[shown_idx]["text"]}</div>',
                unsafe_allow_html=True,
            )
            st.divider()

        if current_level < len(hints) - 1:
            st.button(
                "Reveal Next Hint",
                key=f"hint_btn_{current_idx}_{current_level}",
                use_container_width=True,
                on_click=advance_hint,
            )
        else:
            st.caption("All hints revealed.")


def _render_progress_panel() -> None:
    chapters: dict[int, list] = {}
    for idx, exercise in enumerate(st.session_state.exercises):
        chapter = exercise["metadata"]["chapter"]
        chapters.setdefault(chapter, []).append((idx, exercise))

    tab_labels = [f"Ch {ch}" for ch in sorted(chapters)]
    tabs = st.tabs(tab_labels)

    for tab, (_ch, items) in zip(tabs, sorted(chapters.items()), strict=False):
        with tab:
            for idx, exercise in items:
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
                    f"{theme_name} &middot; {success_count}/{MASTERY_THRESHOLD}"
                    f"</div>",
                    unsafe_allow_html=True,
                )


def _render_pep_tip() -> None:
    current_exercise = get_current_exercise()
    tip = current_exercise.get("pep_tip", "Keep your code clean and readable!")
    st.markdown('<div class="section-title">PEP8</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pep-tip-box">{tip}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DIALOGS
# ═══════════════════════════════════════════════════════════════


@st.dialog("Reset All Progress", width="small")
def _reset_dialog() -> None:
    st.warning("Erase all progress, scores, and hint levels?")
    st.caption("Your localStorage data will be cleared. This cannot be undone.")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Cancel", use_container_width=True):
            st.session_state.show_reset_dialog = False
            st.rerun(scope="app")
    with c2:
        if st.button("Reset Everything", type="primary", use_container_width=True):
            st.session_state.show_reset_dialog = False
            reset_all_progress()


# ═══════════════════════════════════════════════════════════════
# NAVIGATION CALLBACKS
# ═══════════════════════════════════════════════════════════════


def _navigate_previous() -> None:
    previous_exercise()
    save_progress()


def _navigate_next() -> None:
    next_exercise()
    save_progress()


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════


def render_app() -> None:
    initialize_session_state()

    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "show_reset_dialog" not in st.session_state:
        st.session_state.show_reset_dialog = False

    st.html(f"<style>{_theme_css()}</style>")

    _render_header()
    _render_stats_bar()

    left, right = st.columns([2, 1])

    with left:
        _render_exercise_prompt()
        _render_code_editor()
        _render_test_result()
        _render_action_buttons()

    with right:
        _render_progress_panel()
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        _render_pep_tip()
        st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
        if st.button("🗑 Reset All Progress", use_container_width=True):
            st.session_state.show_reset_dialog = True

    if st.session_state.show_reset_dialog:
        _reset_dialog()

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)
    st.markdown(
        '<div class="footer-text">'
        f"{MASTERY_THRESHOLD} successes unlock mastery."
        "</div>",
        unsafe_allow_html=True,
    )

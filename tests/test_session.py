import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.session import (
    DEFAULT_LIVES,
    HINT_PENALTY,
    MASTERY_THRESHOLD,
    POINTS_PER_SUCCESS,
    STORAGE_KEY,
    advance_hint,
    get_current_exercise,
    get_current_hint_level,
    load_progress,
    next_exercise,
    previous_exercise,
    reset_exercise_code,
    save_progress,
)


def _make_exercise(idx: int) -> dict:
    return {
        "id": f"ex_{idx:03d}",
        "metadata": {"chapter": 1, "theme": "test"},
        "content": {"prompt": f"prompt {idx}", "initial_code": f"code {idx}"},
        "hints": [
            {"level": "basic", "text": "hint1"},
            {"level": "detailed", "text": "hint2"},
            {"level": "solution", "text": "hint3"},
        ],
    }


def _to_session_state(exercises: list[dict]) -> SimpleNamespace:
    num = len(exercises)
    return SimpleNamespace(
        exercises=exercises,
        successes=[0] * num,
        attempts=[0] * num,
        score=0,
        lives=DEFAULT_LIVES,
        current_exercise_idx=0,
        hint_levels=[-1] * num,
        user_code=exercises[0]["content"]["initial_code"],
    )


def _patch_session_state(state: SimpleNamespace):
    return patch("app.session.st.session_state", state, create=True)


# ---------------------------------------------------------------------------
# load_progress / save_progress
# ---------------------------------------------------------------------------


class TestProgressPersistence:
    def test_load_progress_returns_none_for_empty_store(self):
        with patch("app.session.get_local_storage", return_value=None):
            assert load_progress() is None

    def test_load_progress_returns_parsed_state(self):
        data = '{"score": 150, "lives": 2}'
        with patch("app.session.get_local_storage", return_value=data):
            result = load_progress()
            assert result == {"score": 150, "lives": 2}

    def test_load_progress_ignores_corrupted_json(self):
        with patch("app.session.get_local_storage", return_value="{bad"):
            assert load_progress() is None

    def test_save_progress_calls_set_local_storage(self):
        mock_set = MagicMock()
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        with (
            patch("app.session.set_local_storage", mock_set),
            _patch_session_state(state),
        ):
            save_progress()
        mock_set.assert_called_once()
        args = mock_set.call_args[0]
        assert args[0] == STORAGE_KEY
        parsed = json.loads(args[1])
        assert parsed["score"] == 0
        assert parsed["lives"] == DEFAULT_LIVES
        assert parsed["successes"] == [0, 0]


# ---------------------------------------------------------------------------
# navigation
# ---------------------------------------------------------------------------


class TestNavigation:
    def test_next_exercise_advances_index(self):
        exercises = [_make_exercise(i) for i in range(3)]
        state = _to_session_state(exercises)
        with _patch_session_state(state):
            next_exercise()
        assert state.current_exercise_idx == 1
        assert state.user_code == "code 1"

    def test_next_exercise_stays_at_last(self):
        exercises = [_make_exercise(i) for i in range(3)]
        state = _to_session_state(exercises)
        state.current_exercise_idx = 2
        with _patch_session_state(state):
            next_exercise()
        assert state.current_exercise_idx == 2

    def test_previous_exercise_decrements_index(self):
        exercises = [_make_exercise(i) for i in range(3)]
        state = _to_session_state(exercises)
        state.current_exercise_idx = 2
        with _patch_session_state(state):
            previous_exercise()
        assert state.current_exercise_idx == 1
        assert state.user_code == "code 1"

    def test_previous_exercise_stays_at_first(self):
        exercises = [_make_exercise(i) for i in range(3)]
        state = _to_session_state(exercises)
        with _patch_session_state(state):
            previous_exercise()
        assert state.current_exercise_idx == 0

    def test_reset_exercise_code_restores_initial(self):
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        state.user_code = "modified"
        with _patch_session_state(state):
            reset_exercise_code()
        assert state.user_code == "code 0"

    def test_get_current_exercise(self):
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        with _patch_session_state(state):
            ex = get_current_exercise()
        assert ex["id"] == "ex_000"


# ---------------------------------------------------------------------------
# hint system
# ---------------------------------------------------------------------------


class TestHints:
    @staticmethod
    def _patched(state):
        return _patch_session_state(state), patch(
            "app.session.set_local_storage", MagicMock()
        )

    def test_advance_hint_returns_first_hint(self):
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        state.score = 50
        with (
            _patch_session_state(state),
            patch("app.session.set_local_storage", MagicMock()),
        ):
            hint = advance_hint()
        assert hint == "hint1"
        assert state.hint_levels[0] == 0
        assert state.score == 50 - HINT_PENALTY

    def test_advance_hint_returns_second_hint(self):
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        state.hint_levels[0] = 0
        with (
            _patch_session_state(state),
            patch("app.session.set_local_storage", MagicMock()),
        ):
            hint = advance_hint()
        assert hint == "hint2"
        assert state.hint_levels[0] == 1

    def test_advance_hint_deducts_points(self):
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        state.score = 100
        with (
            _patch_session_state(state),
            patch("app.session.set_local_storage", MagicMock()),
        ):
            advance_hint()
        assert state.score == 100 - HINT_PENALTY

    def test_advance_hint_score_floors_to_zero(self):
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        state.score = 5
        with (
            _patch_session_state(state),
            patch("app.session.set_local_storage", MagicMock()),
        ):
            advance_hint()
        assert state.score == 0

    def test_advance_hint_returns_none_when_exhausted(self):
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        state.hint_levels[0] = 2
        with (
            _patch_session_state(state),
            patch("app.session.set_local_storage", MagicMock()),
        ):
            hint = advance_hint()
        assert hint is None

    def test_get_current_hint_level_default(self):
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        with _patch_session_state(state):
            assert get_current_hint_level() == -1

    def test_get_current_hint_level_after_advance(self):
        exercises = [_make_exercise(0), _make_exercise(1)]
        state = _to_session_state(exercises)
        with (
            _patch_session_state(state),
            patch("app.session.set_local_storage", MagicMock()),
        ):
            advance_hint()
            assert get_current_hint_level() == 0


# ---------------------------------------------------------------------------
# mastery constants
# ---------------------------------------------------------------------------


class TestMastery:
    def test_mastery_threshold_is_3(self):
        assert MASTERY_THRESHOLD == 3

    def test_points_per_success_is_50(self):
        assert POINTS_PER_SUCCESS == 50

    def test_default_lives_is_3(self):
        assert DEFAULT_LIVES == 3

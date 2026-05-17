REQUIRED_TOP_KEYS = {
    "id",
    "metadata",
    "content",
    "validation",
    "hints",
    "pep_tip",
    "boss",
}
REQUIRED_METADATA_KEYS = {
    "chapter",
    "concept",
    "subconcept",
    "difficulty",
    "theme",
    "prerequisites",
    "tags",
}
REQUIRED_CONTENT_KEYS = {"prompt", "initial_code"}
REQUIRED_VALIDATION_KEYS = {"tests"}


class TestExerciseData:
    def test_all_exercises_have_required_top_keys(self, exercises):
        for ex in exercises:
            missing = REQUIRED_TOP_KEYS - set(ex.keys())
            assert not missing, f"{ex['id']} missing top-level keys: {missing}"

    def test_all_exercises_have_required_metadata_keys(self, exercises):
        for ex in exercises:
            meta = ex.get("metadata", {})
            missing = REQUIRED_METADATA_KEYS - set(meta.keys())
            assert not missing, f"{ex['id']} missing metadata keys: {missing}"

    def test_all_exercises_have_required_content_keys(self, exercises):
        for ex in exercises:
            content = ex.get("content", {})
            missing = REQUIRED_CONTENT_KEYS - set(content.keys())
            assert not missing, f"{ex['id']} missing content keys: {missing}"

    def test_all_exercises_have_required_validation_keys(self, exercises):
        for ex in exercises:
            validation = ex.get("validation", {})
            missing = REQUIRED_VALIDATION_KEYS - set(validation.keys())
            assert not missing, f"{ex['id']} missing validation keys: {missing}"

    def test_hints_is_nonempty_list(self, exercises):
        for ex in exercises:
            hints = ex.get("hints", [])
            assert (
                isinstance(hints, list) and len(hints) > 0
            ), f"{ex['id']} has no hints"
            for hint in hints:
                assert (
                    "level" in hint and "text" in hint
                ), f"{ex['id']} hint missing level/text"

    def test_boss_is_bool(self, exercises):
        for ex in exercises:
            assert isinstance(ex["boss"], bool), f"{ex['id']} boss field must be bool"

    def test_difficulty_is_valid(self, exercises):
        valid = {"beginner", "intermediate", "advanced"}
        for ex in exercises:
            assert (
                ex["metadata"]["difficulty"] in valid
            ), f"{ex['id']} invalid difficulty"

    def test_prerequisites_are_valid_refs(self, exercises, exercise_dict):
        for ex in exercises:
            for prereq in ex["metadata"].get("prerequisites", []):
                assert (
                    prereq in exercise_dict
                ), f"{ex['id']} prereq '{prereq}' not found"

    def test_tags_is_list_of_strings(self, exercises):
        for ex in exercises:
            tags = ex["metadata"].get("tags", [])
            assert isinstance(tags, list), f"{ex['id']} tags must be list"
            assert all(
                isinstance(t, str) for t in tags
            ), f"{ex['id']} tags must be strings"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import yaml

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_exercise(ref: str) -> dict:
    path = _DATA_DIR / "exercises" / f"{ref}.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_solution(ref: str) -> str:
    path = _DATA_DIR / "solutions" / f"{ref}.py"
    return path.read_text(encoding="utf-8")


def load_index() -> list[str]:
    path = _DATA_DIR / "index.yaml"
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [entry["ref"] for entry in data["exercises"]]


@pytest.fixture
def exercise_refs():
    return load_index()


@pytest.fixture
def exercises(exercise_refs):
    return [load_exercise(ref) for ref in exercise_refs]


@pytest.fixture
def exercise_dict(exercises):
    return {ex["id"]: ex for ex in exercises}


@pytest.fixture
def solutions(exercise_refs):
    return {ref: load_solution(ref) for ref in exercise_refs}

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

import pytest
import yaml


def load_exercise(ref: str) -> dict:
    path = Path(__file__).parent.parent / "data" / "exercises" / f"{ref}.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_solution(ref: str) -> str:
    path = Path(__file__).parent.parent / "data" / "solutions" / f"{ref}.py"
    return path.read_text(encoding="utf-8")


def load_index() -> list[str]:
    path = Path(__file__).parent.parent / "data" / "index.yaml"
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

from pathlib import Path

import yaml

from app.engine import execute_code_with_tests


def _load_exercise(ref: str) -> dict:
    path = Path(__file__).parent.parent / "data" / "exercises" / f"{ref}.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_solution(ref: str) -> str:
    path = Path(__file__).parent.parent / "data" / "solutions" / f"{ref}.py"
    return path.read_text(encoding="utf-8")


def _load_index() -> list[str]:
    path = Path(__file__).parent.parent / "data" / "index.yaml"
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [entry["ref"] for entry in data["exercises"]]


class TestExerciseSolutions:
    def test_each_solution_passes_its_own_tests(self):
        for ref in _load_index():
            exercise = _load_exercise(ref)
            solution_code = _load_solution(ref)
            test_code = exercise["validation"]["tests"]

            result = execute_code_with_tests(solution_code, test_code)
            assert result["success"] is True, (
                f"{ref} solution failed its own tests:\n"
                f"  Solution: {solution_code.strip()}\n"
                f"  Message: {result['message']}"
            )

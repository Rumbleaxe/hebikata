from app.engine import execute_code_with_tests


class TestExerciseSolutions:
    def test_each_solution_passes_its_own_tests(
        self, exercise_refs, exercise_dict, solutions
    ):
        for ref in exercise_refs:
            exercise = exercise_dict[ref]
            solution_code = solutions[ref]
            test_code = exercise["validation"]["tests"]

            result = execute_code_with_tests(solution_code, test_code)
            assert result["success"] is True, (
                f"{ref} solution failed its own tests:\n"
                f"  Solution: {solution_code.strip()}\n"
                f"  Message: {result['message']}"
            )

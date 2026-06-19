"""
HebiKata - Code Execution Engine

Provides the execute_code_with_tests() function that runs user-provided
Python code in an isolated namespace and validates it against test functions.

Security Note:
    Uses exec() in isolated namespace. In production, consider additional
    sandboxing (e.g., RestrictedPython) for untrusted user input.
"""

import traceback
from typing import Any


def execute_code_with_tests(user_code: str, test_code: str) -> dict[str, Any]:
    """
    Execute user code and run pytest tests against it.

    This function safely executes user-provided Python code in an isolated
    namespace, then runs pytest test functions against it to validate the
    solution. Both code and tests execute in the same namespace to allow
    tests to access user-defined variables.

    Args:
        user_code: The user's Python code to execute and test
        test_code: The pytest test function code (must define function
                   starting with 'test_')

    Returns:
        Dict[str, Any]: Result dictionary with keys:
            - success (bool): True if all tests passed, False otherwise
            - message (str): User-friendly success/failure message
            - error (str or None): Detailed error traceback if failed, None if success
    """
    namespace: dict[str, Any] = {}

    try:
        exec(user_code, namespace)
        exec(test_code, namespace)

        test_funcs = [
            obj
            for name, obj in namespace.items()
            if name.startswith("test_") and callable(obj)
        ]

        if not test_funcs:
            return {
                "success": False,
                "message": "No test function found",
                "error": "Test code must define a function starting with test_",
            }

        for test_func in test_funcs:
            test_func()

        return {"success": True, "message": "✅ All tests passed!", "error": None}

    except AssertionError as e:
        return {
            "success": False,
            "message": f"❌ Test failed: {str(e)}",
            "error": str(e),
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error: {type(e).__name__}",
            "error": traceback.format_exc(),
        }

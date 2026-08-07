"""
HebiKata - Code Execution Engine

Provides the execute_code_with_tests() function that runs user-provided
Python code in a sandboxed namespace and validates it against test functions.
"""

import traceback
from typing import Any

_SAFE_BUILTINS: dict[str, Any] = {
    "True": True,
    "False": False,
    "None": None,
    "Ellipsis": Ellipsis,
    "NotImplemented": NotImplemented,
    # type constructors
    "bool": bool,
    "int": int,
    "float": float,
    "complex": complex,
    "str": str,
    "bytes": bytes,
    "bytearray": bytearray,
    "list": list,
    "tuple": tuple,
    "dict": dict,
    "set": set,
    "frozenset": frozenset,
    "object": object,
    "type": type,
    "slice": slice,
    "range": range,
    "memoryview": memoryview,
    # conversions / representations
    "abs": abs,
    "bin": bin,
    "chr": chr,
    "hex": hex,
    "oct": oct,
    "ord": ord,
    "repr": repr,
    "format": format,
    "ascii": ascii,
    "hash": hash,
    "id": id,
    # math
    "divmod": divmod,
    "max": max,
    "min": min,
    "pow": pow,
    "round": round,
    "sum": sum,
    # iteration / sequencing
    "all": all,
    "any": any,
    "enumerate": enumerate,
    "filter": filter,
    "iter": iter,
    "len": len,
    "map": map,
    "next": next,
    "reversed": reversed,
    "sorted": sorted,
    "zip": zip,
    # introspection (safe)
    "callable": callable,
    "getattr": getattr,
    "hasattr": hasattr,
    "isinstance": isinstance,
    "issubclass": issubclass,
    "vars": vars,
    "dir": dir,
    # output (harmless)
    "print": print,
    # property / decorators
    "property": property,
    "staticmethod": staticmethod,
    "classmethod": classmethod,
    "super": super,
    # exceptions
    "BaseException": BaseException,
    "Exception": Exception,
    "ArithmeticError": ArithmeticError,
    "AssertionError": AssertionError,
    "AttributeError": AttributeError,
    "EOFError": EOFError,
    "ImportError": ImportError,
    "IndexError": IndexError,
    "KeyError": KeyError,
    "KeyboardInterrupt": KeyboardInterrupt,
    "LookupError": LookupError,
    "MemoryError": MemoryError,
    "NameError": NameError,
    "NotImplementedError": NotImplementedError,
    "OSError": OSError,
    "OverflowError": OverflowError,
    "RecursionError": RecursionError,
    "ReferenceError": ReferenceError,
    "RuntimeError": RuntimeError,
    "StopAsyncIteration": StopAsyncIteration,
    "StopIteration": StopIteration,
    "SyntaxError": SyntaxError,
    "SystemError": SystemError,
    "TypeError": TypeError,
    "UnboundLocalError": UnboundLocalError,
    "UnicodeError": UnicodeError,
    "ValueError": ValueError,
    "ZeroDivisionError": ZeroDivisionError,
}


def execute_code_with_tests(user_code: str, test_code: str) -> dict[str, Any]:
    """
    Execute user code and run test functions against it in a sandboxed namespace.

    Args:
        user_code: The user's Python code to execute and test.
        test_code: Test function code (must define a function starting with 'test_').

    Returns:
        Dict with keys:
            - success (bool): True if all tests passed.
            - message (str): User-friendly success/failure message.
            - error (str | None): Error traceback if failed, None if success.
    """
    namespace: dict[str, Any] = {"__builtins__": _SAFE_BUILTINS}

    try:
        exec(user_code, namespace)
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error: {type(e).__name__}",
            "error": traceback.format_exc(),
        }

    try:
        exec(test_code, namespace)
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error: {type(e).__name__}",
            "error": traceback.format_exc(),
        }

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

    try:
        for test_func in test_funcs:
            test_func()
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

    return {"success": True, "message": "✅ All tests passed!", "error": None}

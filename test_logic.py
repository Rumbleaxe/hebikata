"""
Simple test to verify exercise execution logic.
"""

import sys
sys.path.insert(0, 'app')

from main import execute_code_with_tests

# Test 1: Successful test
print("Test 1: Successful execution")
user_code = "mana = 100"
test_code = """
def test_mana():
    assert mana == 100, "Fireball needs 100 mana!"
"""
result = execute_code_with_tests(user_code, test_code)
print(f"  Result: {result}")
assert result['success'] == True, "Expected success"
print("  ✅ PASSED\n")

# Test 2: Failed assertion
print("Test 2: Failed assertion")
user_code = "mana = 50"
test_code = """
def test_mana():
    assert mana == 100, "Fireball needs 100 mana!"
"""
result = execute_code_with_tests(user_code, test_code)
print(f"  Result: {result}")
assert result['success'] == False, "Expected failure"
assert "Fireball needs 100 mana!" in result['message']
print("  ✅ PASSED\n")

# Test 3: Syntax error
print("Test 3: Syntax error")
user_code = "mana = "
test_code = """
def test_mana():
    assert mana == 100
"""
result = execute_code_with_tests(user_code, test_code)
print(f"  Result: {result}")
assert result['success'] == False, "Expected failure"
print("  ✅ PASSED\n")

# Test 4: String test
print("Test 4: String variable")
user_code = 'decrypt_key = "skRM9x"'
test_code = """
def test_key():
    assert decrypt_key == "skRM9x", "Access denied"
"""
result = execute_code_with_tests(user_code, test_code)
print(f"  Result: {result}")
assert result['success'] == True, "Expected success"
print("  ✅ PASSED\n")

print("=" * 50)
print("All tests passed! ✅")
print("=" * 50)

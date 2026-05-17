from main import execute_code_with_tests


class TestSuccessfulExecution:
    def test_simple_assignment(self):
        result = execute_code_with_tests(
            "mana = 100",
            "def test_mana():\n    assert mana == 100, 'Fireball needs 100 mana!'",
        )
        assert result["success"] is True

    def test_string_variable(self):
        result = execute_code_with_tests(
            'decrypt_key = "skRM9x"',
            "def test_key():\n    assert decrypt_key == 'skRM9x', 'Access denied'",
        )
        assert result["success"] is True

    def test_float_precision(self):
        result = execute_code_with_tests(
            "neutron_mass = 1.675e-27",
            "def test_neutron():\n    assert abs(neutron_mass - 1.675e-27) < 1e-28",
        )
        assert result["success"] is True

    def test_hex_literal(self):
        result = execute_code_with_tests(
            "nonce = 0xdeadbeef",
            "def test_nonce():\n    assert hex(nonce) == '0xdeadbeef'",
        )
        assert result["success"] is True


class TestFailedExecution:
    def test_failed_assertion(self):
        result = execute_code_with_tests(
            "mana = 50",
            "def test_mana():\n    assert mana == 100, 'Fireball needs 100 mana!'",
        )
        assert result["success"] is False
        assert "Fireball needs 100 mana!" in result["message"]

    def test_syntax_error(self):
        result = execute_code_with_tests(
            "mana = ", "def test_mana():\n    assert mana == 100"
        )
        assert result["success"] is False
        assert "SyntaxError" in result.get("error", "")


class TestEdgeCases:
    def test_empty_user_code(self):
        result = execute_code_with_tests("", "def test_nothing():\n    assert True")
        assert result["success"] is True

    def test_no_test_function(self):
        result = execute_code_with_tests("x = 1", "x = 2")
        assert result["success"] is False
        assert "No test function found" in result["message"]

    def test_multiple_test_functions_first_passes_second_fails(self):
        result = execute_code_with_tests(
            "x = 1",
            "def test_a():\n    assert x == 1\ndef test_b():\n    assert x == 2",
        )
        assert result["success"] is False

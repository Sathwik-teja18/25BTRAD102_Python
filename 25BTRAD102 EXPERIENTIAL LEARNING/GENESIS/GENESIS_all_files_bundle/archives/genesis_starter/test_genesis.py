"""Offline smoke tests for GENESIS helpers. Does not call Ollama."""
import importlib.util
import unittest
from pathlib import Path

SOURCE = Path(__file__).with_name("genesis.py")
spec = importlib.util.spec_from_file_location("genesis_under_test", SOURCE)
genesis = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(genesis)


class GenesisHelperTests(unittest.TestCase):
    def test_seed_cortex_is_valid(self):
        kernel = object.__new__(genesis.ImmutableKernel)
        valid, report = kernel.validate_cortex(genesis.SEED_CORTEX)
        self.assertTrue(valid, report)

    def test_valid_plugin_signature(self):
        source = "def can_handle(text):\n    return text == 'hello'\n\ndef execute(text, kernel):\n    return 'hi'\n"
        kernel = object.__new__(genesis.ImmutableKernel)
        valid, report = kernel.validate_skill(source)
        self.assertTrue(valid, report)

    def test_plugin_missing_entrypoint_rejected(self):
        source = "def execute(text, kernel):\n    return 'hi'\n"
        kernel = object.__new__(genesis.ImmutableKernel)
        valid, report = kernel.validate_skill(source)
        self.assertFalse(valid)
        self.assertIn("can_handle", report)

    def test_dangerous_call_rejected(self):
        source = "def can_handle(text):\n    return True\n\ndef execute(text, kernel):\n    return eval(text)\n"
        valid, report = genesis.validate_python_source(source, ("can_handle", "execute"))
        self.assertFalse(valid)
        self.assertIn("eval", report)

    def test_model_tiers(self):
        self.assertEqual(genesis.ImmutableKernel.task_tier("debug this Python traceback"), "coding")
        self.assertEqual(genesis.ImmutableKernel.task_tier("prove this theorem step by step"), "reasoning")
        self.assertEqual(genesis.ImmutableKernel.task_tier("hello there"), "general")

    def test_extract_code_block(self):
        code = genesis.extract_python_code("```python\ndef example():\n    return 3\n```\n")
        self.assertIn("def example", code)
        self.assertNotIn("```", code)

    def test_json_parser(self):
        parsed = genesis.parse_json_object('{"action": "answer", "response": "ok"}')
        self.assertEqual(parsed["action"], "answer")


if __name__ == "__main__":
    unittest.main(verbosity=2)

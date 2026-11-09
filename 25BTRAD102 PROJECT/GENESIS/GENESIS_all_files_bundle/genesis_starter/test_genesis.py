"""Offline smoke tests for GENESIS helpers. Does not call Ollama."""
import importlib.util
import json
import unittest
from pathlib import Path
from unittest import mock

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

    def test_online_chat_does_not_send_saved_memory(self):
        kernel = object.__new__(genesis.ImmutableKernel)
        kernel.load_memory = lambda: {"notes": [{"fact": "private saved note"}]}

        class FakeProvider:
            model = "test-online-model"

            def chat(self, messages, **_kwargs):
                self.messages = messages
                return '{"action":"answer","response":"hello"}'

        provider = FakeProvider()
        with mock.patch.object(
            genesis.OpenAIProvider,
            "from_environment",
            return_value=provider,
        ):
            result = kernel.route_request("hello")

        self.assertEqual(result["response"], "hello")
        self.assertNotIn(
            "private saved note",
            json.dumps(provider.messages),
        )
        self.assertEqual(result["model"], "openai:test-online-model")

    def test_code_generation_stays_on_local_model(self):
        kernel = object.__new__(genesis.ImmutableKernel)
        kernel.available_models = ["local-model"]
        kernel.resolve_model = lambda _tier: "local-model"
        kernel._request_json = lambda *_args, **_kwargs: {
            "message": {"content": "local result"}
        }

        with mock.patch.object(
            genesis.OpenAIProvider,
            "from_environment",
            side_effect=AssertionError("code requests must not use OpenAI"),
        ):
            for prompt, purpose in (
                ("rewrite this Python function", "coding"),
                ("```js\nconst greeting = 1;\n```", None),
            ):
                with self.subTest(prompt=prompt):
                    result = kernel.llm_query(
                        [{"role": "user", "content": prompt}],
                        purpose=purpose,
                    )
                    self.assertEqual(result, "local result")
                    self.assertEqual(kernel.last_model, "local-model")

    def test_chat_falls_back_to_local_after_online_provider_failure(self):
        kernel = object.__new__(genesis.ImmutableKernel)
        kernel.available_models = ["local-model"]
        kernel.load_memory = lambda: {"notes": []}
        kernel.resolve_model = lambda _tier: "local-model"
        kernel._request_json = lambda *_args, **_kwargs: {
            "message": {
                "content": (
                    '{"action":"answer","response":"local answer"}'
                )
            }
        }

        class FakeProvider:
            model = "test-online-model"

            def chat(self, *_args, **_kwargs):
                raise RuntimeError("offline")

        with mock.patch.object(
            genesis.OpenAIProvider,
            "from_environment",
            return_value=FakeProvider(),
        ):
            result = kernel.route_request("hello")

        self.assertEqual(result["response"], "local answer")
        self.assertEqual(result["model"], "local-model")


if __name__ == "__main__":
    unittest.main(verbosity=2)

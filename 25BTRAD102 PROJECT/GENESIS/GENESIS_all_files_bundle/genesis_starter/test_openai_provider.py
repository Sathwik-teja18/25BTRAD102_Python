"""Offline tests for OpenAI provider configuration and budget accounting."""

import json
import tempfile
import unittest
import urllib.error
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from openai_provider import (
    DailyBudgetExceeded,
    OpenAIProvider,
    ProviderConfigurationError,
)


class OpenAIProviderTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.ledger_path = Path(self.temporary_directory.name) / "usage.json"

    def make_provider(
        self,
        *,
        input_price="10",
        output_price="20",
        daily_budget="1",
    ):
        return OpenAIProvider(
            api_key="test-key",
            model="test-model",
            input_usd_per_million=Decimal(input_price),
            output_usd_per_million=Decimal(output_price),
            daily_budget_usd=Decimal(daily_budget),
            ledger_path=self.ledger_path,
        )

    @staticmethod
    def response(payload):
        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return json.dumps(payload).encode("utf-8")

        return FakeResponse()

    @staticmethod
    def fake_opener(response=None, error=None):
        class FakeOpener:
            def open(self, *_args, **_kwargs):
                if error is not None:
                    raise error
                return response

        return FakeOpener()

    def test_chat_records_actual_usage_and_releases_reservation(self):
        provider = self.make_provider()
        payload = {
            "choices": [{"message": {"content": '{"action":"answer"}'}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        }
        with patch(
            "openai_provider.urllib.request.build_opener",
            return_value=self.fake_opener(self.response(payload)),
        ):
            result = provider.chat(
                [{"role": "user", "content": "hello"}],
                temperature=0.2,
                json_mode=True,
                max_tokens=100,
            )

        self.assertEqual(result, '{"action":"answer"}')
        ledger = json.loads(self.ledger_path.read_text(encoding="utf-8"))
        self.assertEqual(Decimal(ledger["spent_usd"]), Decimal("0.0002"))
        self.assertEqual(Decimal(ledger["reserved_usd"]), Decimal(0))

    def test_over_budget_request_is_rejected_before_network_call(self):
        provider = self.make_provider(
            input_price="10000",
            output_price="10000",
            daily_budget="1",
        )
        with patch("openai_provider.urllib.request.build_opener") as build_opener:
            with self.assertRaises(DailyBudgetExceeded):
                provider.chat(
                    [{"role": "user", "content": "hello"}],
                    temperature=0.2,
                    json_mode=False,
                    max_tokens=1000,
                )
        build_opener.assert_not_called()

    def test_pricing_changes_are_rejected_after_daily_usage_is_reserved(self):
        first_provider = self.make_provider()
        first_provider._reserve(Decimal("0.001"))
        changed_provider = self.make_provider(input_price="11")

        with self.assertRaisesRegex(RuntimeError, "pricing, or budget changed"):
            changed_provider._reserve(Decimal("0.001"))

    def test_transport_failure_keeps_reservation_for_uncertain_charge(self):
        provider = self.make_provider()
        with patch(
            "openai_provider.urllib.request.build_opener",
            return_value=self.fake_opener(error=urllib.error.URLError("offline")),
        ):
            with self.assertRaisesRegex(RuntimeError, "OpenAI request failed"):
                provider.chat(
                    [{"role": "user", "content": "hello"}],
                    temperature=0.2,
                    json_mode=False,
                    max_tokens=100,
                )

        ledger = json.loads(self.ledger_path.read_text(encoding="utf-8"))
        self.assertGreater(Decimal(ledger["reserved_usd"]), Decimal(0))

    def test_missing_usage_keeps_reservation_for_the_day(self):
        provider = self.make_provider()
        payload = {"choices": [{"message": {"content": "answer"}}]}
        with patch(
            "openai_provider.urllib.request.build_opener",
            return_value=self.fake_opener(self.response(payload)),
        ):
            with self.assertRaisesRegex(RuntimeError, "omitted usage data"):
                provider.chat(
                    [{"role": "user", "content": "hello"}],
                    temperature=0.2,
                    json_mode=False,
                    max_tokens=100,
                )

        ledger = json.loads(self.ledger_path.read_text(encoding="utf-8"))
        self.assertGreater(Decimal(ledger["reserved_usd"]), Decimal(0))

    def test_environment_configuration_requires_explicit_prices(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ProviderConfigurationError, "GENESIS_OPENAI_API_KEY"):
                OpenAIProvider.from_environment(self.ledger_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)

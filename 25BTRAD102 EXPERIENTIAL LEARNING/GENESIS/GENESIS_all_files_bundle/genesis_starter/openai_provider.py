"""OpenAI chat provider with a persisted client-side daily budget guard."""

from __future__ import annotations

import datetime as dt
import json
import os
import tempfile
import threading
import urllib.error
import urllib.request
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


_LEDGER_THREAD_LOCK = threading.Lock()


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_args, **_kwargs):
        return None


class ProviderConfigurationError(RuntimeError):
    pass


class DailyBudgetExceeded(RuntimeError):
    pass


class OpenAIProvider:
    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        input_usd_per_million: Decimal,
        output_usd_per_million: Decimal,
        daily_budget_usd: Decimal,
        ledger_path: Path,
        timeout: int = 120,
    ) -> None:
        if not api_key.strip() or not model.strip():
            raise ProviderConfigurationError("OpenAI API key and model are required.")
        if (
            not input_usd_per_million.is_finite()
            or not output_usd_per_million.is_finite()
            or input_usd_per_million <= 0
            or output_usd_per_million <= 0
        ):
            raise ProviderConfigurationError(
                "OpenAI input and output prices must both be greater than zero."
            )
        if not daily_budget_usd.is_finite() or daily_budget_usd <= 0:
            raise ProviderConfigurationError("Daily budget must be greater than zero.")

        self.api_key = api_key.strip()
        self.model = model.strip()
        self.input_usd_per_million = input_usd_per_million
        self.output_usd_per_million = output_usd_per_million
        self.daily_budget_usd = daily_budget_usd
        self.ledger_path = ledger_path
        self.lock_path = ledger_path.with_suffix(ledger_path.suffix + ".lock")
        self.timeout = timeout

    @classmethod
    def from_environment(cls, ledger_path: Path) -> OpenAIProvider:
        required = {
            "GENESIS_OPENAI_API_KEY": os.environ.get("GENESIS_OPENAI_API_KEY"),
            "GENESIS_OPENAI_MODEL": os.environ.get("GENESIS_OPENAI_MODEL"),
            "GENESIS_OPENAI_INPUT_USD_PER_1M": os.environ.get(
                "GENESIS_OPENAI_INPUT_USD_PER_1M"
            ),
            "GENESIS_OPENAI_OUTPUT_USD_PER_1M": os.environ.get(
                "GENESIS_OPENAI_OUTPUT_USD_PER_1M"
            ),
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ProviderConfigurationError(
                "OpenAI is not configured. Set: " + ", ".join(missing)
            )

        try:
            input_price = Decimal(
                required["GENESIS_OPENAI_INPUT_USD_PER_1M"] or ""
            )
            output_price = Decimal(
                required["GENESIS_OPENAI_OUTPUT_USD_PER_1M"] or ""
            )
            daily_budget = Decimal(os.environ.get("GENESIS_DAILY_BUDGET_USD", "1.00"))
        except (InvalidOperation, TypeError) as exc:
            raise ProviderConfigurationError(
                "OpenAI prices and daily budget must be valid decimal amounts."
            ) from exc

        return cls(
            api_key=required["GENESIS_OPENAI_API_KEY"] or "",
            model=required["GENESIS_OPENAI_MODEL"] or "",
            input_usd_per_million=input_price,
            output_usd_per_million=output_price,
            daily_budget_usd=daily_budget,
            ledger_path=ledger_path,
        )

    @staticmethod
    def _utc_date() -> str:
        return dt.datetime.now(dt.timezone.utc).date().isoformat()

    @contextmanager
    def _ledger_lock(self):
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with _LEDGER_THREAD_LOCK:
            with self.lock_path.open("a+b") as lock_file:
                if os.name == "nt":
                    import msvcrt

                    lock_file.seek(0)
                    if lock_file.read(1) == b"":
                        lock_file.seek(0)
                        lock_file.write(b"\0")
                        lock_file.flush()
                    lock_file.seek(0)
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
                    try:
                        yield
                    finally:
                        lock_file.seek(0)
                        msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
                    try:
                        yield
                    finally:
                        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    def _read_ledger(self) -> dict[str, Any]:
        today = self._utc_date()
        try:
            value = json.loads(self.ledger_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            value = {}
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Could not read usage ledger: {exc}") from exc

        if not isinstance(value, dict):
            raise RuntimeError("Usage ledger has an invalid format.")
        if value.get("date_utc") != today:
            return {"date_utc": today, "spent_usd": "0", "reserved_usd": "0"}
        try:
            spent = Decimal(value["spent_usd"])
            reserved = Decimal(value["reserved_usd"])
            if (
                not spent.is_finite()
                or not reserved.is_finite()
                or spent < 0
                or reserved < 0
            ):
                raise ValueError("Amounts must be finite and nonnegative.")
        except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
            raise RuntimeError("Usage ledger contains invalid amounts.") from exc
        return value

    def _write_ledger(self, value: dict[str, Any]) -> None:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary_name = tempfile.mkstemp(
            prefix=f".{self.ledger_path.name}.",
            suffix=".tmp",
            dir=str(self.ledger_path.parent),
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                json.dump(value, handle, indent=2)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_name, self.ledger_path)
        except Exception:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
            raise

    def _price(self, input_tokens: int, output_tokens: int) -> Decimal:
        return (
            Decimal(input_tokens) * self.input_usd_per_million
            + Decimal(output_tokens) * self.output_usd_per_million
        ) / Decimal(1_000_000)

    def _reserve(self, amount: Decimal) -> None:
        with self._ledger_lock():
            ledger = self._read_ledger()
            spent = Decimal(ledger["spent_usd"])
            reserved = Decimal(ledger["reserved_usd"])
            configuration = {
                "model": self.model,
                "input_usd_per_million": str(
                    self.input_usd_per_million.normalize()
                ),
                "output_usd_per_million": str(
                    self.output_usd_per_million.normalize()
                ),
                "daily_budget_usd": str(self.daily_budget_usd.normalize()),
            }
            stored_configuration = ledger.get("pricing")
            if stored_configuration is None:
                if spent or reserved:
                    raise RuntimeError(
                        "Usage ledger has spend without pricing metadata; "
                        "online calls are disabled until the next UTC day."
                    )
                ledger["pricing"] = configuration
            elif stored_configuration != configuration:
                raise RuntimeError(
                    "OpenAI model, pricing, or budget changed during the current UTC day. "
                    "Restore the original settings or wait for the next UTC day."
                )
            if spent + reserved + amount > self.daily_budget_usd:
                raise DailyBudgetExceeded(
                    f"Online daily budget of ${self.daily_budget_usd} would be exceeded."
                )
            ledger["reserved_usd"] = str(reserved + amount)
            self._write_ledger(ledger)

    def _settle(self, reservation: Decimal, actual_cost: Decimal) -> None:
        with self._ledger_lock():
            ledger = self._read_ledger()
            reserved = Decimal(ledger["reserved_usd"])
            spent = Decimal(ledger["spent_usd"])
            ledger["reserved_usd"] = str(max(Decimal(0), reserved - reservation))
            ledger["spent_usd"] = str(spent + actual_cost)
            self._write_ledger(ledger)

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float,
        json_mode: bool,
        max_tokens: int,
    ) -> str:
        if max_tokens <= 0:
            raise ValueError("Maximum completion tokens must be greater than zero.")
        request = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "temperature": temperature,
            "max_completion_tokens": max_tokens,
        }
        if json_mode:
            request["response_format"] = {"type": "json_object"}

        # Reserve conservatively before sending anything to the paid provider.
        serialized_bytes = len(
            json.dumps(request, ensure_ascii=False).encode("utf-8")
        )
        input_token_bound = serialized_bytes + 512
        reservation = self._price(input_token_bound, max_tokens)
        self._reserve(reservation)

        http_request = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(request).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            opener = urllib.request.build_opener(_NoRedirectHandler)
            with opener.open(http_request, timeout=self.timeout) as response:
                result: Any = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(f"OpenAI request failed: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(
                "OpenAI response could not be read; the reserved budget remains "
                "unavailable for today."
            ) from exc

        try:
            usage = result["usage"]
            input_tokens = int(usage["prompt_tokens"])
            output_tokens = int(usage["completion_tokens"])
            content = result["choices"][0]["message"]["content"]
            if input_tokens < 0 or output_tokens < 0 or not isinstance(content, str):
                raise ValueError("Unexpected usage or message content.")
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            # Keep the full reservation: the provider may have billed this request.
            raise RuntimeError(
                "OpenAI returned an invalid response or omitted usage data; "
                "the reserved budget remains unavailable for today."
            ) from exc

        actual_cost = self._price(input_tokens, output_tokens)
        self._settle(reservation, actual_cost)
        return content

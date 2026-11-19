
"""
GENESIS - Local AI Assistant
Version 4.1.0

Requirements:
    Python 3.10+
    Ollama installed and running
    Optional: pip install psutil

Files:
    genesis.py
    cortex.py
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from cortex import AGENT_NAME, AGENT_VERSION, handle_request


# ============================================================
# Configuration
# ============================================================

DEFAULT_MODEL = "qwen3.5:4b"
MEMORY_FILE = Path(__file__).resolve().parent / "genesis_memory.json"


def normalize_ollama_url(value=None):
    """Normalize Ollama's base URL for client requests."""
    value = (
        value
        or os.environ.get("GENESIS_OLLAMA_URL")
        or os.environ.get("OLLAMA_HOST")
        or "http://127.0.0.1:11434"
    ).strip().rstrip("/")

    if "://" not in value:
        value = "http://" + value

    from urllib.parse import urlsplit, urlunsplit

    parts = urlsplit(value)

    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError(
            f"Invalid Ollama URL: {value!r}. "
            "Use http://127.0.0.1:11434"
        )

    if parts.hostname == "0.0.0.0":
        port = parts.port or 11434
        netloc = f"127.0.0.1:{port}"
        parts = parts._replace(netloc=netloc)

    return urlunsplit((
        parts.scheme,
        parts.netloc,
        parts.path.rstrip("/"),
        "",
        "",
    ))


OLLAMA_HOST = normalize_ollama_url()


# ============================================================
# GENESIS kernel
# ============================================================

class GenesisKernel:
    def __init__(self):
        
self.model = os.environ.get("GENESIS_MODEL", DEFAULT_MODEL)
self.default_model = self.model
self.auto_model_routing = True
self.ollama_host = OLLAMA_HOST
self.running = True
self.conversation = []
self._available_model_names = None


    # --------------------------------------------------------
    # HTTP helper
    # --------------------------------------------------------

    def api_request(self, endpoint, payload=None, timeout=60):
        """Send a JSON request to the local Ollama API."""
        url = f"{self.ollama_host}{endpoint}"

        data = None
        headers = {"Accept": "application/json"}

        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method="POST" if data is not None else "GET",
        )

        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")

        return json.loads(raw) if raw.strip() else {}

    # --------------------------------------------------------
    # Persistent memory
    # --------------------------------------------------------

    def load_memory(self):
        if not MEMORY_FILE.exists():
            return {"notes": []}

        try:
            with MEMORY_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                return {"notes": []}

            data.setdefault("notes", [])
            return data

        except (OSError, json.JSONDecodeError):
            print("[MEMORY] Could not read memory file; using empty memory.")
            return {"notes": []}

    def save_memory(self, memory):
        temporary = MEMORY_FILE.with_suffix(".tmp")

        with temporary.open("w", encoding="utf-8") as file:
            json.dump(memory, file, indent=2, ensure_ascii=False)

        temporary.replace(MEMORY_FILE)

    # --------------------------------------------------------
    # Ollama connectivity and models
    # --------------------------------------------------------

    def check_connection(self):
        try:
            self.api_request("/api/tags", timeout=5)
            return True
        except Exception:
            return False

    def list_models(self):
        try:
            data = self.api_request("/api/tags", timeout=10)
            models = data.get("models", [])

            if not models:
                print("[MODELS] No models installed.")
                print("Use: pull model qwen3.5:4b")
                return

            print("\nInstalled Ollama models")
            print("-" * 32)

            for model in models:
                name = model.get("name", "unknown")
                size = model.get("size", 0)
                size_gb = size / (1024 ** 3)
                print(f"  {name} ({size_gb:.2f} GB)")

            print()

        except Exception as exc:
            print(f"[ERROR] Could not list models: {exc}")
            self.show_connection_help()

    def pull_model(self, model_name):
        model_name = model_name.strip()

        if not model_name:
            print("Usage: pull model MODEL_NAME")
            return

        if any(ch.isspace() for ch in model_name):
            print("[ERROR] Model name must not contain spaces.")
            return

        print(
            f"Download model '{model_name}' from Ollama? "
            "Downloads may be several GB."
        )

        try:
            answer = input("Continue? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n[CANCELLED] Download cancelled.")
            return

        if answer not in {"y", "yes"}:
            print("[CANCELLED] Download cancelled.")
            return

        print(f"[MODEL] Pulling {model_name}. Progress follows.")

        request_data = json.dumps({
            "name": model_name,
            "stream": True,
        }).encode("utf-8")

        request = urllib.request.Request(
            f"{self.ollama_host}/api/pull",
            data=request_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=3600) as response:
                for raw_line in response:
                    line = raw_line.decode("utf-8").strip()

                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        print(line)
                        continue

                    status = event.get("status", "")
                    completed = event.get("completed")
                    total = event.get("total")

                    if isinstance(completed, (int, float)) and isinstance(
                        total, (int, float)
                    ) and total > 0:
                        percent = completed * 100 / total
                        print(
                            f"\r[MODEL] {status}: {percent:.1f}%",
                            end="",
                            flush=True,
                        )
                    elif status:
                        print(f"\n[MODEL] {status}")

                    if event.get("error"):
                        raise RuntimeError(event["error"])

            print(f"\n[SUCCESS] Model '{model_name}' downloaded.")
            self.model = model_name

        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            print(f"\n[ERROR] Ollama returned HTTP {exc.code}.")
            if detail:
                print(detail)

        except urllib.error.URLError as exc:
            print(f"\n[ERROR] Could not contact Ollama: {exc.reason}")
            self.show_connection_help()

        except Exception as exc:
            print(f"\n[ERROR] Model download failed: {exc}")

    # --------------------------------------------------------
    # Chat
    # --------------------------------------------------------
    
    # --------------------------------------------------------
    # Adaptive model routing
    # --------------------------------------------------------

    def get_available_model_names(self):
        """Read and cache the models currently installed in Ollama."""
        if self._available_model_names is not None:
            return self._available_model_names

        try:
            result = self.api_request("/api/tags", timeout=10)
            self._available_model_names = {
                item.get("name", "")
                for item in result.get("models", [])
                if item.get("name")
            }
        except Exception as exc:
            print(f"[ROUTER] Could not list models: {exc}")
            self._available_model_names = set()

        return self._available_model_names

    @staticmethod
    def assess_prompt_strength(prompt):
        """
        Heuristic complexity estimate, not a learned intelligence score.
        Returns fast, balanced, or advanced.
        """
        text = prompt.lower()

        # When cortex adds development instructions, assess the
        # original request rather than the entire wrapper.
        marker = "original user request:"
        if marker in text:
            text = text.rsplit(marker, 1)[-1].strip()

        words = text.split()
        score = 0

        advanced_phrases = (
            "step by step",
            "multi-step",
            "in depth",
            "comprehensive",
            "architecture",
            "system design",
            "optimize",
            "optimization",
            "prove that",
            "mathematical proof",
            "debug",
            "traceback",
            "stack trace",
            "refactor",
            "integrate",
            "implement",
            "train a model",
            "neural network",
            "machine learning",
            "create a new skill",
            "build a module",
            "preserve existing features",
            "analyze this code",
        )

        balanced_phrases = (
            "explain",
            "compare",
            "summarize",
            "difference between",
            "how does",
            "why does",
            "pros and cons",
            "give examples",
        )

        score += sum(
            3 for phrase in advanced_phrases if phrase in text
        )

        score += sum(
            1 for phrase in balanced_phrases if phrase in text
        )

        # Longer requests may need more context, but length alone
        # does not automatically make a request advanced.
        if len(words) > 100:
            score += 1
        if len(words) > 250:
            score += 1

        if "```" in text or "traceback (most recent call last)" in text:
            score += 3

        if any(
            term in text
            for term in (" and then ", "multiple files", "several steps")
        ):
            score += 1

        if score >= 3:
            return "advanced"
        if score >= 1:
            return "balanced"
        return "fast"

    def select_model_for_prompt(self, prompt):
        """Choose an installed model without changing manual preference."""
        if not self.auto_model_routing:
            return self.model, "manual"

        tier = self.assess_prompt_strength(prompt)
        candidates = MODEL_TIERS[tier]
        available = self.get_available_model_names()

        # Prefer models from the requested tier that are installed.
        if available:
            for candidate in candidates:
                if candidate in available:
                    return candidate, tier

            # If no tier candidate is available, use the configured
            # model when installed.
            if self.default_model in available:
                return self.default_model, "fallback"

            # Last resort: use any installed model.
            if available:
                chosen = sorted(available)[0]
                return chosen, "fallback"

        # If model discovery failed, use the configured model.
        return self.default_model, "fallback"

    def route_request(self, prompt):
        """Send a normal user prompt to Ollama."""
        if not self.check_connection():
            return {
                "status": "SUCCESS",
                "response": (
                    "I cannot reach Ollama at "
                    f"{self.ollama_host}.\n"
                    "Start Ollama and try again."
                ),
            }

        
        selected_model, routing_tier = self.select_model_for_prompt(prompt)

        print(
            f"[ROUTER] Tier: {routing_tier} | "
            f"Model: {selected_model}"
        )

        messages = list(self.conversation)
        messages.append({"role": "user", "content": prompt})


        try:
            result = self.api_request(
                "/api/chat",
                {
                    "model": selected_model,
                    "messages": messages,
                    "stream": False,
                },
                timeout=600,
            )

            message = result.get("message", {})
            response_text = message.get("content", "").strip()

            if not response_text:
                response_text = "The model returned an empty response."

            self.conversation.append({
                "role": "user",
                "content": prompt,
            })
            self.conversation.append({
                "role": "assistant",
                "content": response_text,
            })

            # Keep recent context bounded.
            self.conversation = self.conversation[-20:]

            return {
                "status": "SUCCESS",
                "response": response_text,
            }

        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            return {
                "status": "SUCCESS",
                "response": (
                    f"Ollama returned HTTP {exc.code}.\n{detail}"
                ),
            }

        except urllib.error.URLError as exc:
            return {
                "status": "SUCCESS",
                "response": (
                    f"Could not connect to Ollama: {exc.reason}\n"
                    "Check that Ollama is running."
                ),
            }

        except Exception as exc:
            return {
                "status": "SUCCESS",
                "response": f"Chat error: {exc}",
            }

    # --------------------------------------------------------
    # Help and command handling
    # --------------------------------------------------------

    def show_connection_help(self):
        print(
            "\nCheck that Ollama is installed and running.\n"
            f"Configured URL: {self.ollama_host}\n"
            "Test in PowerShell:\n"
            '  Invoke-RestMethod "http://127.0.0.1:11434/api/tags"\n'
        )

    def show_help(self):
        print("""
GENESIS COMMANDS
----------------
/help                    Show this help
/models                  List installed Ollama models
/pull MODEL_NAME         Download a model
/model MODEL_NAME        Switch the chat model
/clear                   Clear conversation context
/stats                   Show CPU, RAM and battery
/exit                    Exit GENESIS

Natural-language commands:
  stats
  cpu usage
  ram usage
  battery percentage
  time
  os
  remember your note
  memory

You can also type any normal message to chat with Ollama.
""")

    def handle_user_input(self, user_input):
        command = user_input.strip()

        
        if low == "/auto":
            self.auto_model_routing = not self.auto_model_routing
            mode = "ON" if self.auto_model_routing else "OFF"
            print(f"[ROUTER] Automatic model routing: {mode}")
            return

        if low in {"/auto on", "/auto off"}:
            self.auto_model_routing = low.endswith("on")
            mode = "ON" if self.auto_model_routing else "OFF"
            print(f"[ROUTER] Automatic model routing: {mode}")
            return

        if not command:
            return

        low = command.lower()

        if low in {"/exit", "exit", "quit"}:
            self.running = False
            print("[GENESIS] Goodbye.")
            return

        if low in {"/help", "help"}:
            self.show_help()
            return

        if low in {"/models", "models"}:
            self.list_models()
            return

        if low.startswith("/pull "):
            self.pull_model(command[6:].strip())
            return

        if low.startswith("pull model "):
            self.pull_model(command[len("pull model "):].strip())
            return

        if low.startswith("/model "):
            model_name = command[7:].strip()
            if model_name:
                self.model = model_name
                self.conversation.clear()
                print(f"[MODEL] Active model set to {self.model}")
            else:
                print("Usage: /model MODEL_NAME")
            return

        if low == "/clear":
            self.conversation.clear()
            print("[GENESIS] Conversation context cleared.")
            return

        # Route hardware, memory, time and OS commands through cortex.py.
        result = handle_request(command, self)

        if result.get("status") == "EVOLVE":
            print("[GENESIS] Evolution is not implemented in this recovery build.")
            return

        response = result.get("response", "")

        if response:
            print(f"\nGENESIS > {response}\n")
        else:
            print("[GENESIS] No response returned.")

    # --------------------------------------------------------
    # Main loop
    # --------------------------------------------------------

    def execute_loop(self):
        print("=" * 52)
        print(f"{AGENT_NAME} v{AGENT_VERSION}")
        print("Local AI assistant powered by Ollama")
        print("=" * 52)
        print(f"Ollama URL: {self.ollama_host}")
        print(f"Selected model: {self.model}")

        if self.check_connection():
            print("[OLLAMA] Connected.")
        else:
            print("[OLLAMA] Not reachable yet.")
            print("Start Ollama or check its local API URL.")

        print("Type /help for commands or /exit to quit.\n")

        while self.running:
            try:
                user_input = input("You > ")
                self.handle_user_input(user_input)

            except KeyboardInterrupt:
                print("\n[GENESIS] Interrupted. Type /exit to quit.")
                continue

            except EOFError:
                print("\n[GENESIS] Input closed. Goodbye.")
                break

            except Exception as exc:
                print(f"\n[ERROR] Unexpected error: {exc}")


def main():
    try:
        kernel = GenesisKernel()
        kernel.execute_loop()
    except Exception as exc:
        print(f"[STARTUP ERROR] {exc}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()

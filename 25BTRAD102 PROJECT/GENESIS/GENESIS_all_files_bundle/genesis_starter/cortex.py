"""GENESIS Cortex: mutable request routing and basic capabilities."""
import datetime
import json
import platform

AGENT_NAME = "GENESIS"
AGENT_VERSION = "4.0.0"


def handle_request(user_input: str, kernel) -> dict:
    """Required entry point. Return SUCCESS, EVOLVE, or TERMINAL actions."""
    command = user_input.strip()
    low = command.lower()

    if low.startswith("remember "):
        fact = command[len("remember "):].strip()
        if not fact:
            return {"status": "SUCCESS", "response": "Tell me what to remember after 'remember'."}
        memory = kernel.load_memory()
        memory.setdefault("notes", []).append({
            "fact": fact,
            "time": datetime.datetime.now().isoformat(timespec="seconds"),
        })
        kernel.save_memory(memory)
        return {"status": "SUCCESS", "response": f"Saved to persistent memory: {fact}"}

    if low in {"memory", "what do you remember", "show memory"}:
        memory = kernel.load_memory()
        facts = [item.get("fact", str(item)) for item in memory.get("notes", [])]
        return {"status": "SUCCESS", "response": "Memory notes:\n" + ("\n".join(f"- {x}" for x in facts) if facts else "(none yet)")}

    if low in {"time", "what time is it", "date and time"}:
        now = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        return {"status": "SUCCESS", "response": f"Local system time: {now}"}

    if low in {"os", "system info", "operating system"}:
        info = f"{platform.system()} {platform.release()} ({platform.machine()})"
        return {"status": "SUCCESS", "response": f"Host OS: {info}"}

    # Example of an input that the starter brain deliberately does not know yet.
    if low in {"stats", "system stats", "hardware stats", "cpu usage", "what is my cpu usage?"}:
        return {
            "status": "EVOLVE",
            "objective": (
                "Add a hardware telemetry capability triggered by 'stats', 'system stats', "
                "'hardware stats', or CPU-usage questions. Prefer psutil for CPU and RAM "
                "percentages and battery percentage when available. Handle a missing psutil "
                "package gracefully with clear installation instructions; do not run installers "
                "automatically. Preserve all current commands and the required entry point."
            ),
        }

    return kernel.route_request(command)

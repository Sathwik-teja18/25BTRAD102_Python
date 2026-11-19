
"""GENESIS Cortex: request routing and hardware telemetry."""

import datetime
import platform
import re

AGENT_NAME = "GENESIS"
AGENT_VERSION = "4.1.0"


def get_hardware_stats() -> dict:
    """Return CPU, RAM, and battery information using psutil if available."""
    try:
        import psutil
    except ImportError:
        return {
            "status": "SUCCESS",
            "response": (
                "Hardware telemetry is unavailable because psutil is not "
                "installed.\n\n"
                "To enable it, run this command in your terminal:\n"
                "python -m pip install psutil\n\n"
                "Restart GENESIS after installation."
            ),
        }

    lines = ["GENESIS Hardware Telemetry", "=" * 28]

    # CPU usage
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        lines.append(f"CPU usage: {cpu_percent:.1f}%")
    except Exception:
        lines.append("CPU usage: Unavailable")

    # RAM usage
    try:
        memory = psutil.virtual_memory()
        used_gb = (memory.total - memory.available) / (1024 ** 3)
        total_gb = memory.total / (1024 ** 3)

        lines.append(
            f"RAM usage: {memory.percent:.1f}% "
            f"({used_gb:.2f} / {total_gb:.2f} GB)"
        )
    except Exception:
        lines.append("RAM usage: Unavailable")

    # Battery percentage
    try:
        battery = psutil.sensors_battery()

        if battery is None:
            lines.append(
                "Battery: No battery detected or battery telemetry unavailable"
            )
        else:
            charging = " (charging)" if battery.power_plugged else ""
            lines.append(f"Battery: {battery.percent:.1f}%{charging}")
    except Exception:
        lines.append("Battery: Unavailable")

    return {
        "status": "SUCCESS",
        "response": "\n".join(lines),
    }


def handle_request(user_input: str, kernel) -> dict:
    """Required entry point for the GENESIS kernel."""
    command = user_input.strip()
    low = command.lower().strip()
    normalized = re.sub(r"\s+", " ", low).rstrip("?!., ")

    # ---------------------------------------------------------------
    # Persistent memory: remember a fact
    # ---------------------------------------------------------------
    if low.startswith("remember "):
        fact = command[len("remember "):].strip()

        if not fact:
            return {
                "status": "SUCCESS",
                "response": "Tell me what to remember after 'remember'.",
            }

        memory = kernel.load_memory()
        memory.setdefault("notes", []).append({
            "fact": fact,
            "time": datetime.datetime.now().isoformat(
                timespec="seconds"
            ),
        })
        kernel.save_memory(memory)

        return {
            "status": "SUCCESS",
            "response": f"Saved to persistent memory: {fact}",
        }

    # ---------------------------------------------------------------
    # Persistent memory: list saved facts
    # ---------------------------------------------------------------
    if normalized in {
        "memory",
        "what do you remember",
        "show memory",
    }:
        memory = kernel.load_memory()
        facts = [
            item.get("fact", str(item))
            for item in memory.get("notes", [])
        ]

        return {
            "status": "SUCCESS",
            "response": (
                "Memory notes:\n"
                + (
                    "\n".join(f"- {fact}" for fact in facts)
                    if facts
                    else "(none yet)"
                )
            ),
        }

    # ---------------------------------------------------------------
    # Local time and date
    # ---------------------------------------------------------------
    if normalized in {
        "time",
        "what time is it",
        "date and time",
    }:
        now = datetime.datetime.now().astimezone().strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        )

        return {
            "status": "SUCCESS",
            "response": f"Local system time: {now}",
        }

    # ---------------------------------------------------------------
    # Operating system information
    # ---------------------------------------------------------------
    if normalized in {
        "os",
        "system info",
        "operating system",
    }:
        info = (
            f"{platform.system()} {platform.release()} "
            f"({platform.machine()})"
        )

        return {
            "status": "SUCCESS",
            "response": f"Host OS: {info}",
        }

    # ---------------------------------------------------------------
    # Hardware telemetry: direct commands
    # ---------------------------------------------------------------
    direct_stats_commands = {
        "stats",
        "system stats",
        "hardware stats",
        "hardware telemetry",
        "cpu",
        "cpu usage",
        "processor usage",
        "ram",
        "ram usage",
        "memory usage",
        "battery",
        "battery percentage",
        "battery level",
        "what is my cpu usage",
        "what's my cpu usage",
        "what is my ram usage",
        "what is my memory usage",
        "what is my battery percentage",
    }

    if normalized in direct_stats_commands:
        return get_hardware_stats()

    # ---------------------------------------------------------------
    # Hardware telemetry: natural-language questions
    # ---------------------------------------------------------------
    hardware_terms = (
        "cpu usage",
        "processor usage",
        "ram usage",
        "memory usage",
        "battery percentage",
        "battery level",
        "hardware stats",
        "system stats",
        "hardware telemetry",
    )

    question_starters = (
        "what",
        "how",
        "show",
        "check",
        "display",
        "get",
        "tell me",
    )

    asks_about_hardware = any(
        term in normalized for term in hardware_terms
    )

    asks_for_measurement = any(
        term in normalized
        for term in (
            "usage",
            "percentage",
            "percent",
            "level",
            "stats",
            "telemetry",
        )
    )

    is_question_or_command = normalized.startswith(question_starters)

    if (
        asks_about_hardware
        and (asks_for_measurement or is_question_or_command)
    ):
        return get_hardware_stats()

    # ---------------------------------------------------------------
    # Preserve general-purpose routing through the existing kernel
    # ---------------------------------------------------------------
    return kernel.route_request(command)

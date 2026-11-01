"""
USN: 25BTRAD102
LAB EXERCISE 11: LOG FILE READER PROGRAM

QUESTION:
Develop a Python program to read a log file, identify keywords such as
ERROR, WARNING, and INFO, and summarize the number of occurrences of each.

CRITICAL THINKING (CT):
Analyze log contents, design search and counting logic, handle missing or
empty files, and verify the accuracy of results.

REAL WORLD EXPOSURE (RWE):
Apply the program to a sample application log and explain how it helps
identify errors and monitor system activity.

INPUT:
Create a text file named application.log in the same directory. Put log
entries in it, using ERROR, WARNING, and INFO labels.
"""

from pathlib import Path

LOG_FILE = Path(__file__).with_name("application.log")
KEYWORDS = ("ERROR", "WARNING", "INFO")


def summarize_log(file_path):
    counts = {keyword: 0 for keyword in KEYWORDS}

    try:
        with file_path.open("r", encoding="utf-8") as log_file:
            for line in log_file:
                upper_line = line.upper()
                for keyword in KEYWORDS:
                    if keyword in upper_line:
                        counts[keyword] += 1
    except FileNotFoundError:
        print(f"Log file not found: {file_path}")
        return None
    except OSError as error:
        print(f"Unable to read log file: {error}")
        return None

    return counts


def main():
    if not LOG_FILE.exists():
        print(f"Create {LOG_FILE.name} in this folder and add log entries.")
        return

    if LOG_FILE.stat().st_size == 0:
        print("The log file is empty.")
        return

    counts = summarize_log(LOG_FILE)
    if counts is not None:
        print("LOG SUMMARY")
        for keyword, count in counts.items():
            print(f"{keyword}: {count}")


if __name__ == "__main__":
    main()

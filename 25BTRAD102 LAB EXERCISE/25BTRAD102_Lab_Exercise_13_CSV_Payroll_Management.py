"""
USN: 25BTRAD102
LAB EXERCISE 13: CSV-BASED PAYROLL MANAGEMENT SYSTEM

QUESTION:
Develop a Python program to read employee records from a CSV file, calculate
gross salary and applicable deductions, and generate salary summaries.

CRITICAL THINKING (CT):
Analyze payroll requirements, design calculation logic, process CSV records,
validate data, and verify salary calculations.

REAL WORLD EXPOSURE (RWE):
Apply the program to a sample organization's payroll process and interpret
the generated salary summaries.

INPUT:
Create employees.csv in the same directory with the following header:
employee_id,name,basic_salary,allowance,deduction_rate
Enter one employee per row. deduction_rate is a percentage from 0 to 100.
"""

import csv
from pathlib import Path

CSV_FILE = Path(__file__).with_name("employees.csv")
REQUIRED_FIELDS = {
    "employee_id", "name", "basic_salary", "allowance", "deduction_rate"
}


def read_payroll(file_path):
    employees = []
    with file_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not REQUIRED_FIELDS.issubset(reader.fieldnames):
            raise ValueError("CSV is missing one or more required column headers.")

        for line_number, row in enumerate(reader, start=2):
            try:
                basic = float(row["basic_salary"])
                allowance = float(row["allowance"])
                rate = float(row["deduction_rate"])
            except (TypeError, ValueError):
                raise ValueError(f"Invalid numeric value on CSV line {line_number}.")

            if basic < 0 or allowance < 0 or not 0 <= rate <= 100:
                raise ValueError(f"Invalid salary or deduction rate on line {line_number}.")
            if not row["employee_id"].strip() or not row["name"].strip():
                raise ValueError(f"Missing employee ID or name on line {line_number}.")

            gross = basic + allowance
            deduction = gross * rate / 100
            net = gross - deduction
            employees.append({
                "employee_id": row["employee_id"].strip(),
                "name": row["name"].strip(),
                "gross": gross,
                "deduction": deduction,
                "net": net
            })

    return employees


def main():
    if not CSV_FILE.exists():
        print(f"Input file not found: {CSV_FILE.name}")
        print("Create it with the required column headers and employee records.")
        return

    try:
        employees = read_payroll(CSV_FILE)
    except (OSError, ValueError) as error:
        print(f"Unable to process payroll: {error}")
        return

    if not employees:
        print("The CSV file contains no employee records.")
        return

    print("\nPAYROLL SUMMARY")
    print(f'{"ID":<12} {"Name":<20} {"Gross":>12} {"Deduction":>12} {"Net":>12}')
    print("-" * 72)

    total_gross = total_deductions = total_net = 0.0
    for employee in employees:
        print(
            f'{employee["employee_id"]:<12} {employee["name"]:<20} '
            f'{employee["gross"]:>12.2f} {employee["deduction"]:>12.2f} '
            f'{employee["net"]:>12.2f}'
        )
        total_gross += employee["gross"]
        total_deductions += employee["deduction"]
        total_net += employee["net"]

    print("-" * 72)
    print(f"Employees processed: {len(employees)}")
    print(f"Total gross salary: {total_gross:.2f}")
    print(f"Total deductions: {total_deductions:.2f}")
    print(f"Total net salary: {total_net:.2f}")


if __name__ == "__main__":
    main()

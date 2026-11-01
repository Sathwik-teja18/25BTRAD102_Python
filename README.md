# 25BTRAD102_Python

Python programming assignments, laboratory exercises, and mini-projects completed for **USN: 25BTRAD102**.

The repository contains interactive Python programs, with task descriptions and requirements documented in each source file. The programs are organized using the three existing course directories.

## Repository Structure

```text
25BTRAD102_Python/
├── 25BTRAD102 ASSIGNMENT TASKS/
│   └── 25BTRAD102_Assignment_Task_Unit_I.py
│
├── 25BTRAD102 LAB EXERCISE/
│   ├── 25BTRAD102_Lab_Exercise_1_Python_Setup_and_Basics.py
│   ├── 25BTRAD102_Lab_Exercise_5_Number_Guessing_Game.py
│   ├── 25BTRAD102_Lab_Exercise_6_Prime_and_Factorial.py
│   ├── 25BTRAD102_Lab_Exercise_7_Fibonacci_Recursion.py
│   ├── 25BTRAD102_Lab_Exercise_8_Contact_Book.py
│   ├── 25BTRAD102_Lab_Exercise_9_Student_Grading_System.py
│   ├── 25BTRAD102_Lab_Exercise_10_Frequency_Counter.py
│   ├── 25BTRAD102_Lab_Exercise_11_Log_File_Reader.py
│   ├── 25BTRAD102_Lab_Exercise_12_Student_Data_Manager.py
│   ├── 25BTRAD102_Lab_Exercise_13_CSV_Payroll_Management.py
│   ├── 25BTRAD102_Lab_Exercise_14_Bank_Account_System_OOP.py
│   ├── 25BTRAD102_Lab_Exercise_15_Library_Management_System.py
│   └── 25BTRAD102_Lab_Exercise_16_Dice_Simulator.py
│
└── 25BTRAD102 MINI PROJECT/
    ├── 25BTRAD102_Mini_Project_Attendance_Tracker.py
    ├── 25BTRAD102_Mini_Project_OTP_Generator.py
    ├── 25BTRAD102_Mini_Project_Sales_Data_Analyzer.py
    ├── 25BTRAD102_Mini_Project_Unit_Converter.py
    └── Unit Converter.py
```

## Assignment Tasks

### Unit I Assignment

**File:** `25BTRAD102_Assignment_Task_Unit_I.py`

Includes 18 selectable tasks covering:

- Printing, text formatting, patterns, and comments.
- Variables, data types, and type conversion.
- User input and formatted output.
- Arithmetic operations and basic calculations.
- Celsius-to-Fahrenheit conversion.
- Even/odd number checking.

Run the file and select a task from its menu to execute it individually.

## Laboratory Exercises

| Exercise | Program | Main concepts |
|---|---|---|
| 1 | Python Setup and Basics | Environment setup, variables, operators, input/output, calculator, areas |
| 5 | Number Guessing Game | Loops, conditions, random numbers, input validation |
| 6 | Prime and Factorial | Functions, iteration, mathematical logic |
| 7 | Fibonacci using Recursion | Recursion and memoization |
| 8 | Contact Book | Lists, dictionaries, CRUD operations |
| 9 | Student Grading System | Dictionaries, conditional statements, grade boundaries |
| 10 | Frequency Counter | Dictionaries, counting, text/list processing |
| 11 | Log File Reader | File handling, keyword search, counting |
| 12 | Student Data Manager | CSV file operations, add/search/update/display |
| 13 | CSV Payroll Management | CSV processing, salary calculation, deductions |
| 14 | Bank Account System | Classes, objects, encapsulation, transaction validation |
| 15 | Library Management System | Classes, inheritance, book issue/return status |
| 16 | Dice Simulator | Random module, repeated trials, frequency analysis |

## Mini Projects

| Project | File | Description |
|---|---|---|
| Attendance Tracker | `25BTRAD102_Mini_Project_Attendance_Tracker.py` | Maintain class attendance, update records, and calculate attendance percentages. |
| OTP Generator | `25BTRAD102_Mini_Project_OTP_Generator.py` | Generate and verify time-based one-time passwords using a standalone TOTP implementation. |
| Sales Data Analyzer | `25BTRAD102_Mini_Project_Sales_Data_Analyzer.py` | Maintain product sales, calculate revenue, and identify the highest-selling product by quantity. |
| Unit Converter | `25BTRAD102_Mini_Project_Unit_Converter.py` | Convert distance, temperature, and weight units with input validation. |

## Requirements

- Python 3.8 or later.
- No third-party packages are required for the listed programs.
- The OTP Generator uses Python standard-library modules such as `secrets`, `base64`, `hmac`, `hashlib`, `struct`, and `time`; it does not require `pyotp`.

## Running a Program

1. Install Python and verify the installation:

   ```bash
   python --version
   ```

2. Open a terminal in the repository directory.
3. Run the required Python file. For example:

   ```bash
   python "25BTRAD102 LAB EXERCISE/25BTRAD102_Lab_Exercise_8_Contact_Book.py"
   ```

4. Follow the prompts shown in the terminal.

On some systems, use `python3` instead of `python`.

## Input Files for Selected Exercises

Some programs read or create data files in the same folder as the Python source file:

- **Lab Exercise 11 – Log File Reader:** provide an `application.log` text file containing log entries labelled `ERROR`, `WARNING`, or `INFO`.
- **Lab Exercise 12 – Student Data Manager:** creates and updates `students.csv` automatically.
- **Lab Exercise 13 – CSV Payroll Management:** provide an `employees.csv` file with this exact header:

  ```csv
  employee_id,name,basic_salary,allowance,deduction_rate
  E001,Sample Employee,30000,5000,10
  ```

  The deduction rate is entered as a percentage between 0 and 100.

## OTP Generator Notes

The OTP mini-project implements the time-based one-time password calculation directly:

1. Generates a random shared secret using Python's `secrets` module.
2. Encodes the secret in Base32.
3. Calculates a time counter using a 30-second time step.
4. Applies HMAC-SHA1 and dynamic truncation.
5. Produces a six-digit OTP and verifies codes using constant-time comparison.

**Security:** Treat the generated shared secret as a password. Keep it private, do not commit real account secrets to GitHub, and do not use this educational project as a complete production authentication service without additional security controls.

## Notes

- Program descriptions and task requirements are included in the corresponding Python files.
- Programs are interactive and request input in the terminal.
- Output screenshots are not stored in this repository as part of the Python source files.

---

**USN:** `25BTRAD102`

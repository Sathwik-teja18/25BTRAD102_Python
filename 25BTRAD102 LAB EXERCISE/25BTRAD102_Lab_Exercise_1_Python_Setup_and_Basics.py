"""
USN: 25BTRAD102
LAB EXERCISE 1: PYTHON SETUP, EXECUTION, VARIABLES, OPERATORS, AND I/O

TASK 1 - ENVIRONMENT SETUP NOTES
1. Download and install Python from https://www.python.org/.
2. On Windows, enable "Add Python to PATH" during installation.
3. Verify with: python --version
4. Install Visual Studio Code and the Microsoft Python extension.
5. Install Jupyter with: python -m pip install jupyter
6. Create or open an .ipynb file in VS Code for notebook cells.

TASK 2 - Verify the Python environment with a welcome message.
TASK 3 - Calculate a student's semester percentage.
TASK 4A - Perform basic arithmetic with a simple calculator.
TASK 4B - Calculate rectangle and circle areas.
"""

import math

def read_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def task_2_hello_world():
    print("Hello, World! Python environment is successfully set up.")

def task_3_semester_percentage():
    print("--- Semester Percentage Calculator ---")
    student_name = input("Enter student name: ").strip()
    total_marks = read_number("Enter maximum possible marks: ")
    obtained_marks = read_number("Enter marks obtained: ")
    if total_marks <= 0:
        print("Maximum possible marks must be greater than zero.")
        return
    if obtained_marks < 0 or obtained_marks > total_marks:
        print("Obtained marks must be between 0 and the maximum marks.")
        return
    percentage = obtained_marks / total_marks * 100
    shortfall = total_marks - obtained_marks
    print("\n--- Results ---")
    print(f"Student: {student_name}")
    print(f"Percentage: {percentage:.2f}%")
    print(f"Marks lost: {shortfall:g}")

def task_4a_calculator():
    print("\n--- Simple Calculator ---")
    print("1. Add (+)\n2. Subtract (-)\n3. Multiply (*)\n4. Divide (/)")
    choice = input("Enter choice (1/2/3/4): ").strip()
    if choice not in {"1", "2", "3", "4"}:
        print("Invalid choice.")
        return
    first = read_number("Enter first number: ")
    second = read_number("Enter second number: ")
    if choice == "1":
        result, operator = first + second, "+"
    elif choice == "2":
        result, operator = first - second, "-"
    elif choice == "3":
        result, operator = first * second, "*"
    else:
        if second == 0:
            print("Error: Division by zero is not allowed.")
            return
        result, operator = first / second, "/"
    print(f"Result: {first:g} {operator} {second:g} = {result:g}")

def task_4b_area_calculator():
    print("\n--- Area Calculator ---")
    length = read_number("Enter rectangle length: ")
    width = read_number("Enter rectangle width: ")
    if length < 0 or width < 0:
        print("Length and width cannot be negative.")
        return
    print(f"Area of Rectangle = {length * width:.2f} square units")
    radius = read_number("Enter circle radius: ")
    if radius < 0:
        print("Radius cannot be negative.")
        return
    print(f"Area of Circle = {math.pi * radius ** 2:.2f} square units")

def main():
    while True:
        print("\n--- LAB EXERCISE 1 ---")
        print("1. Hello World / environment verification")
        print("2. Semester percentage calculator")
        print("3. Simple calculator")
        print("4. Area of rectangle and circle")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            task_2_hello_world()
        elif choice == "2":
            task_3_semester_percentage()
        elif choice == "3":
            task_4a_calculator()
        elif choice == "4":
            task_4b_area_calculator()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Enter a number from 1 to 5.")

if __name__ == "__main__":
    main()

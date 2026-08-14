"""Task 1: Installing Python, Setting up VS Code, and Jupyter Notebook
1. Python Installation:
•	Downloaded the latest version of Python from the official website (python.org).
•	Ran the installer and ensured the "Add Python to PATH" checkbox was selected before clicking "Install Now."
•	Verified the installation by opening the command prompt and typing python --version.
2. VS Code Setup:
•	Downloaded and installed Visual Studio Code.
•	Opened VS Code and navigated to the Extensions marketplace (Ctrl+Shift+X).
•	Searched for and installed the official Python extension by Microsoft to enable syntax highlighting, linting, and debugging.
3. Jupyter Notebook Setup:
•	Opened the terminal within VS Code.
•	Installed Jupyter using the Python package manager by running the command: pip install jupyter.
•	Created a new file with a .ipynb extension in VS Code to start writing interactive notebook cells.
"""
"""
Task 2: Write and Execute a Python Program
Objective: Write a basic script to verify the environment setup.
Code:
"""
# Program to print a welcome message and verify execution
def main():
    message = "Hello, World! Python environment is successfully set up."
    print(message)
if __name__ == "__main__":
    main()
#Output:

#Hello, World! Python environment is successfully set up.
"""
Task 3: Programs Using Variables, Operators, and Input/Output
Objective: Demonstrate data types, arithmetic operators, and I/O functions.

Code
"""
# Program to calculate a student's semester percentage
print("--- Semester Percentage Calculator ---")
# Input: Gathering data from the user
student_name = input("Enter student name: ")
total_marks = int(input("Enter maximum possible marks: "))
obtained_marks = int(input("Enter marks obtained: "))
# Variables and Operators: Calculating the result
percentage = (obtained_marks / total_marks) * 100
shortfall = total_marks - obtained_marks
# Output: Displaying the formatted results
print("\n--- Results ---")
print(f"Student: {student_name}")
print(f"Percentage: {percentage:.2f}%")
print(f"Marks lost: {shortfall}")
#Output:
#--- Semester Percentage Calculator ---
#Enter student name: Sathwik
#Enter maximum possible marks: 500
#Enter marks obtained: 462

#--- Results ---
#Student: Sathwik
#Percentage: 92.40%
#Marks lost: 38
"""
Task 4: Simple Calculator and Area Calculation Programs

4A. Simple Calculator
Code:
"""
# Program to perform basic arithmetic operations
def calculator():
    print("Select operation:")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    choice = input("Enter choice (1/2/3/4): ")
    if choice in ['1', '2', '3', '4']:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        if choice == '1':
            print(f"Result: {num1} + {num2} = {num1 + num2}")
        elif choice == '2':
            print(f"Result: {num1} - {num2} = {num1 - num2}")
        elif choice == '3':
            print(f"Result: {num1} * {num2} = {num1 * num2}")
        elif choice == '4':
            if num2 != 0:
                print(f"Result: {num1} / {num2} = {num1 / num2}")
            else:
                print("Error: Division by zero is not allowed.")
    else:
        print("Invalid input.")
calculator()
"""
Output: 
Select operation:
1. Add (+)
2. Subtract (-)
3. Multiply (*)
4. Divide (/)
Enter choice (1/2/3/4): 3
Enter first number: 15
Enter second number: 4
Result: 15.0 * 4.0 = 60.0
"""
"""
4B. Area Calculation Program
Code:
"""
# Program to calculate the area of a circle and a rectangle
import math
def calculate_areas():
    print("--- Area Calculator ---")
    # Rectangle Area
    print("\n1. Rectangle")
    length = float(input("Enter length: "))
    width = float(input("Enter width: "))
    rect_area = length * width
    print(f"Area of Rectangle = {rect_area} sq units")
    # Circle Area
    print("\n2. Circle")
    radius = float(input("Enter radius: "))
    circle_area = math.pi * (radius ** 2)
    print(f"Area of Circle = {circle_area:.2f} sq units")
calculate_areas()
"""
Output:
--- Area Calculator ---
1. Rectangle
Enter length: 12.5
Enter width: 8
Area of Rectangle = 100.0 sq units
2. Circle
Enter radius: 5
Area of Circle = 78.54 sq units
"""
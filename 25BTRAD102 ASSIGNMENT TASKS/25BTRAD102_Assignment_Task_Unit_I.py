"""
USN: 25BTRAD102
PYTHON PROGRAMMING ASSIGNMENT - UNIT I

Contains Tasks 1-18 from the submitted assignment. Select a task from the
menu to run it individually.
"""

def read_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid whole number.")

def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def task_1():
    print("Sathwik Teja Tarikonda")
    print("Computer Science and Engineering")
    print("Jain University")

def task_2():
    for _ in range(3):
        print("*" * 7)

def task_3():
    print("Python is Easy")

def task_4():
    for row in range(1, 6):
        for number in range(1, row + 1):
            print(number, end="")
        print()

def task_5():
    print("Computer\nScience\nEngineering")

def task_6():
    print("Name\tAge\tCity")

def task_7():
    # A comment explains code and is not executed by Python.
    print("Comment executed successfully.")

def task_8():
    explanation = """This is a multi-line explanation.
It spans multiple lines to describe the program clearly
or provide additional information."""
    print("Multi-line comment executed successfully.")
    _ = explanation

def task_9():
    # Initial greeting
    print("Hello!")
    # Secondary message
    print("Welcome to Python.")

def task_10():
    name = "Sathwik Teja Tarikonda"
    print(name)

def task_11():
    var1, var2, var3 = 10, 20, 30
    print(var1, var2, var3)

def task_12():
    string_value = "100"
    integer_value = int(string_value)
    print("Value:", integer_value)
    print("Data Type:", type(integer_value))

def task_13():
    number = 25
    float_number = float(number)
    print("Result:", float_number)
    print("Data Type:", type(float_number))

def task_14():
    age = read_integer("Enter your age: ")
    print("Age displayed as integer:", age)

def task_15():
    first = read_integer("Enter first number: ")
    second = read_integer("Enter second number: ")
    print("Sum:", first + second)

def task_16():
    student_name = input("Enter student's name: ").strip()
    student_age = read_integer("Enter student's age: ")
    student_cgpa = read_float("Enter student's CGPA: ")
    print(f"My name is {student_name}. I am {student_age} years old and my CGPA is {student_cgpa:.2f}.")

def task_17():
    celsius = read_float("Enter temperature in Celsius: ")
    fahrenheit = (celsius * 9 / 5) + 32
    print(f"Temperature in Fahrenheit: {fahrenheit:.2f}")

def task_18():
    number = read_integer("Enter number: ")
    if number % 2 == 0:
        print(f"{number} is Even")
    else:
        print(f"{number} is Odd")

TASKS = {
    "1": ("Print name, department, and college", task_1),
    "2": ("Print a 3 x 7 asterisk pattern", task_2),
    "3": ("Print Python is Easy", task_3),
    "4": ("Print a number triangle", task_4),
    "5": ("Print words on separate lines", task_5),
    "6": ("Demonstrate tab-separated output", task_6),
    "7": ("Demonstrate a single-line comment", task_7),
    "8": ("Demonstrate a multi-line explanation", task_8),
    "9": ("Print greeting messages", task_9),
    "10": ("Print a string variable", task_10),
    "11": ("Print three variables", task_11),
    "12": ("Convert string to integer", task_12),
    "13": ("Convert integer to float", task_13),
    "14": ("Read age as integer", task_14),
    "15": ("Add two integers", task_15),
    "16": ("Display student details", task_16),
    "17": ("Convert Celsius to Fahrenheit", task_17),
    "18": ("Check even or odd", task_18),
}

def main():
    while True:
        print("\n--- PYTHON ASSIGNMENT: UNIT I ---")
        for number, (description, _) in TASKS.items():
            print(f"{number}. {description}")
        print("0. Exit")
        choice = input("Select a task: ").strip()
        if choice == "0":
            break
        selected = TASKS.get(choice)
        if selected is None:
            print("Invalid choice. Select a task from 1 to 18.")
            continue
        print(f"\n--- TASK {choice} ---")
        selected[1]()

if __name__ == "__main__":
    main()

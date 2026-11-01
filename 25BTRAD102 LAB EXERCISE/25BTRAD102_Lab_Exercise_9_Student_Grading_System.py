"""
USN: 25BTRAD102
LAB EXERCISE 9: STUDENT GRADING SYSTEM

QUESTION:
Develop a Python program to store student names and marks using dictionaries,
calculate grades using conditional statements, and display results.

CRITICAL THINKING (CT):
Apply conditional logic, analyze grade boundaries, and verify results using
test cases.

REAL WORLD EXPOSURE (RWE):
Simulate an academic grading scenario and interpret student performance.
"""

students = {}


def calculate_grade(mark):
    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "F"


def add_or_update_student():
    name = input("Enter student name: ").strip()
    if not name:
        print("Student name cannot be empty.")
        return

    try:
        mark = float(input("Enter marks (0-100): "))
    except ValueError:
        print("Marks must be a number.")
        return

    if not 0 <= mark <= 100:
        print("Marks must be between 0 and 100.")
        return

    students[name] = mark
    print("Student record saved.")


def display_results():
    if not students:
        print("No student records available.")
        return

    print("\nSTUDENT RESULTS")
    print(f'{"Name":<25} {"Marks":>8} {"Grade":>8}')
    print("-" * 43)
    for name, mark in students.items():
        print(f"{name:<25} {mark:>8.2f} {calculate_grade(mark):>8}")


def main():
    while True:
        print("\n--- STUDENT GRADING SYSTEM ---")
        print("1. Add or update student marks")
        print("2. Display all results")
        print("3. Search for a student")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_or_update_student()
        elif choice == "2":
            display_results()
        elif choice == "3":
            name = input("Enter student name: ").strip()
            if name in students:
                mark = students[name]
                print(f"Marks: {mark:.2f}; Grade: {calculate_grade(mark)}")
            else:
                print("Student not found.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Enter a number from 1 to 4.")


if __name__ == "__main__":
    main()

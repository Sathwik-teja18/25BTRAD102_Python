"""
USN: 25BTRAD102
LAB EXERCISE 12: STUDENT DATA MANAGER USING FILES

QUESTION:
Develop a Python program to store, retrieve, search, update, and display
student records using file operations.

CRITICAL THINKING (CT):
Design record-management logic, select suitable file operations, validate
inputs, and test data retrieval and updates.

REAL WORLD EXPOSURE (RWE):
Apply the program to a college student-record management scenario and explain
its usefulness in maintaining student information.

INPUT:
Records are stored in students.csv in the same directory. The program creates
the file with a header when it does not already exist.
"""

import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("students.csv")
FIELDNAMES = ["usn", "name", "course"]


def ensure_file():
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_students():
    ensure_file()
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_students(students):
    with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(students)


def add_student():
    usn = input("Enter USN: ").strip()
    name = input("Enter student name: ").strip()
    course = input("Enter course: ").strip()

    if not all((usn, name, course)):
        print("All fields are required.")
        return

    students = load_students()
    if any(student["usn"].casefold() == usn.casefold() for student in students):
        print("A record with this USN already exists.")
        return

    students.append({"usn": usn, "name": name, "course": course})
    save_students(students)
    print("Student record added.")


def search_student():
    usn = input("Enter USN to search: ").strip()
    for student in load_students():
        if student["usn"].casefold() == usn.casefold():
            print(student)
            return
    print("Student record not found.")


def update_student():
    usn = input("Enter USN to update: ").strip()
    students = load_students()

    for student in students:
        if student["usn"].casefold() == usn.casefold():
            name = input("Enter new name (blank to keep current): ").strip()
            course = input("Enter new course (blank to keep current): ").strip()
            if name:
                student["name"] = name
            if course:
                student["course"] = course
            save_students(students)
            print("Student record updated.")
            return

    print("Student record not found.")


def display_students():
    students = load_students()
    if not students:
        print("No student records available.")
        return

    print("\nSTUDENT RECORDS")
    for student in students:
        print(
            f'USN: {student["usn"]} | Name: {student["name"]} | '
            f'Course: {student["course"]}'
        )


def main():
    while True:
        print("\n--- STUDENT DATA MANAGER ---")
        print("1. Add student")
        print("2. Search student")
        print("3. Update student")
        print("4. Display all students")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            search_student()
        elif choice == "3":
            update_student()
        elif choice == "4":
            display_students()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()

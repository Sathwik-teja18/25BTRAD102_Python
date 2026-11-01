"""
USN: 25BTRAD102
MINI PROJECT (UNIT 3): ATTENDANCE TRACKER

PROBLEM STATEMENT:
Develop a Python-based attendance tracker for a class using lists and
dictionaries. Store student names and attendance status, allow attendance
records to be added or updated, display attendance details, and calculate
each student's attendance percentage.

EXPECTED FUNCTIONALITIES:
- Store student names and attendance records using suitable data structures.
- Add students and update their attendance status.
- Display attendance records in an organized format.
- Calculate attendance percentages and identify students below a threshold.
- Test the program using different attendance scenarios.
"""

students = {}
total_classes = 0


def add_student():
    name = input("Enter student name: ").strip()
    if not name:
        print("Student name cannot be empty.")
    elif name.casefold() in (student.casefold() for student in students):
        print("Student already exists.")
    else:
        students[name] = []
        print("Student added.")


def mark_attendance():
    global total_classes

    if not students:
        print("Add students before marking attendance.")
        return

    total_classes += 1
    print(f"Marking attendance for class {total_classes}.")
    for name in students:
        while True:
            status = input(f"{name} (P/A): ").strip().upper()
            if status in ("P", "A"):
                students[name].append(status)
                break
            print("Enter P for present or A for absent.")


def update_attendance():
    if not students or total_classes == 0:
        print("No attendance records are available.")
        return

    name = input("Enter student name: ").strip()
    actual_name = next(
        (student for student in students if student.casefold() == name.casefold()),
        None
    )
    if actual_name is None:
        print("Student not found.")
        return

    try:
        class_number = int(input(f"Enter class number (1-{total_classes}): "))
    except ValueError:
        print("Class number must be an integer.")
        return

    if not 1 <= class_number <= len(students[actual_name]):
        print("Invalid class number.")
        return

    status = input("Enter updated status (P/A): ").strip().upper()
    if status not in ("P", "A"):
        print("Status must be P or A.")
        return

    students[actual_name][class_number - 1] = status
    print("Attendance updated.")


def attendance_percentage(records):
    if not records:
        return 0.0
    return records.count("P") / len(records) * 100


def display_attendance():
    if not students:
        print("No students have been added.")
        return

    print("\nATTENDANCE DETAILS")
    for name, records in students.items():
        present = records.count("P")
        percentage = attendance_percentage(records)
        print(
            f"{name}: Present {present}/{len(records)}, "
            f"Attendance {percentage:.2f}%"
        )


def identify_shortage():
    try:
        threshold = float(input("Enter minimum attendance percentage: "))
    except ValueError:
        print("Enter a valid percentage.")
        return

    if not 0 <= threshold <= 100:
        print("Threshold must be between 0 and 100.")
        return

    below_threshold = [
        (name, attendance_percentage(records))
        for name, records in students.items()
        if attendance_percentage(records) < threshold
    ]

    if not below_threshold:
        print("No students are below the specified threshold.")
    else:
        print("Students below the threshold:")
        for name, percentage in below_threshold:
            print(f"{name}: {percentage:.2f}%")


def main():
    while True:
        print("\n--- ATTENDANCE TRACKER ---")
        print("1. Add student")
        print("2. Mark attendance for a class")
        print("3. Update attendance")
        print("4. Display attendance")
        print("5. Identify students below threshold")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            mark_attendance()
        elif choice == "3":
            update_attendance()
        elif choice == "4":
            display_attendance()
        elif choice == "5":
            identify_shortage()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()

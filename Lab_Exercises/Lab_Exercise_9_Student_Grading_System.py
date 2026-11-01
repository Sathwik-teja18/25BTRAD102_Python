"""Lab Exercise 9: Student Grading System using dictionaries and conditionals."""


def calculate_grade(marks):
    """Return the grade for marks in the inclusive range 0-100."""
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    return "F"


def main():
    students = {}
    try:
        count = int(input("Enter number of students: "))
        if count <= 0:
            print("Enter a positive number of students.")
            return

        for _ in range(count):
            name = input("\\nEnter student name: ").strip()
            if not name:
                print("Name cannot be empty; this entry is skipped.")
                continue
            try:
                marks = float(input("Enter marks (0-100): "))
            except ValueError:
                print("Invalid marks; enter a number. This entry is skipped.")
                continue
            if not 0 <= marks <= 100:
                print("Invalid marks; enter a value from 0 to 100. This entry is skipped.")
                continue
            students[name] = marks

    except ValueError:
        print("Please enter a valid whole number for the student count.")
        return

    print("\\n--- STUDENT RESULTS ---")
    if not students:
        print("No valid student records were entered.")
        return

    for name, marks in students.items():
        print(f"Name: {name} | Marks: {marks:g} | Grade: {calculate_grade(marks)}")


if __name__ == "__main__":
    main()

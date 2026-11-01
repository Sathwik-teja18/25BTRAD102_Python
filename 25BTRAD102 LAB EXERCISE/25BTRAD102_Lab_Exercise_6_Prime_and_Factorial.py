"""
USN: 25BTRAD102
LAB EXERCISE 6: PRIME NUMBER CHECKER AND FACTORIAL CALCULATOR
Part A checks whether an integer is prime. Part B calculates a non-negative
integer's factorial iteratively. Both parts validate their input.
"""
import math

def is_prime(number):
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for divisor in range(3, math.isqrt(number) + 1, 2):
        if number % divisor == 0:
            return False
    return True

def calculate_factorial(number):
    if number < 0:
        raise ValueError("Factorial is not defined for negative integers.")
    result = 1
    for value in range(2, number + 1):
        result *= value
    return result

def read_integer(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Invalid input! Please enter a whole number.")
        return None

def main():
    while True:
        print("\n--- PRIME AND FACTORIAL PROGRAMS ---")
        print("1. Prime number checker\n2. Factorial calculator\n3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            number = read_integer("Enter an integer to check: ")
            if number is not None:
                print(f"{number} is {'a PRIME' if is_prime(number) else 'NOT a prime'} number.")
        elif choice == "2":
            number = read_integer("Enter a non-negative integer: ")
            if number is not None:
                if number < 0:
                    print("Factorial is not defined for negative integers.")
                else:
                    print(f"The factorial of {number} ({number}!) is: {calculate_factorial(number)}")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Enter a number from 1 to 3.")

if __name__ == "__main__":
    main()

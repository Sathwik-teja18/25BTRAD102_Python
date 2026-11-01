"""
USN: 25BTRAD102
LAB EXERCISE 7: FIBONACCI SERIES USING RECURSION
Generate the requested terms recursively. A dictionary memoizes previously
calculated terms to avoid repeated recursive work.
"""

def fibonacci_recursive(n, memo=None):
    if memo is None:
        memo = {0: 0, 1: 1}
    if n < 0:
        raise ValueError("Fibonacci index cannot be negative.")
    if n not in memo:
        memo[n] = fibonacci_recursive(n - 1, memo) + fibonacci_recursive(n - 2, memo)
    return memo[n]

def main():
    print("--- Fibonacci Series Generator (Recursion) ---")
    try:
        terms = int(input("Enter the number of terms you want to print: "))
    except ValueError:
        print("Invalid input! Please enter a whole number.")
        return
    if terms <= 0:
        print("Please enter a positive integer greater than 0.")
        return
    if terms > 1000:
        print("Please enter 1000 terms or fewer to keep the output manageable.")
        return
    print(f"Fibonacci series up to {terms} terms:")
    print(" ".join(str(fibonacci_recursive(index)) for index in range(terms)))

if __name__ == "__main__":
    main()

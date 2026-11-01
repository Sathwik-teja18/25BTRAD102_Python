"""
USN: 25BTRAD102
LAB EXERCISE 16: DICE SIMULATOR USING RANDOM MODULE

QUESTION:
Develop a Python program that simulates rolling one or more dice using
Python's random module. Allow repeated rolls and display the outcomes.

CRITICAL THINKING (CT):
Select suitable random functions, design the simulation logic, test repeated
trials, and analyze the frequency of possible outcomes.

REAL WORLD EXPOSURE (RWE):
Relate the simulation to board games and probability experiments; interpret
the observed outcomes across multiple rolls.
"""

import random
from collections import Counter


def roll_dice(number_of_dice):
    return [random.randint(1, 6) for _ in range(number_of_dice)]


def main():
    try:
        number_of_dice = int(input("Enter number of dice to roll: "))
        number_of_rolls = int(input("Enter number of trials: "))
    except ValueError:
        print("Please enter whole numbers.")
        return

    if number_of_dice < 1 or number_of_rolls < 1:
        print("Both values must be at least 1.")
        return

    outcomes = []
    for trial in range(1, number_of_rolls + 1):
        result = roll_dice(number_of_dice)
        outcomes.append(sum(result))
        print(f"Trial {trial}: Rolls = {result}, Total = {sum(result)}")

    frequencies = Counter(outcomes)
    print("\nFREQUENCY OF TOTALS")
    for total in sorted(frequencies):
        print(f"Total {total}: {frequencies[total]} time(s)")

    print(f"Total trials: {number_of_rolls}")
    print(f"Average total: {sum(outcomes) / number_of_rolls:.2f}")


if __name__ == "__main__":
    main()

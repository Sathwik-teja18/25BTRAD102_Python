"""
USN: 25BTRAD102
LAB EXERCISE 5: NUMBER GUESSING GAME
Choose a secret integer from 1 to 100 and guide the player with higher/lower
hints until it is identified. Invalid input does not consume an attempt.
"""
import random

def play_game():
    lower_bound, upper_bound = 1, 100
    secret_number = random.randint(lower_bound, upper_bound)
    attempts = 0
    print("=" * 58)
    print("Welcome to the Number Guessing Game")
    print("=" * 58)
    print(f"I am thinking of a number between {lower_bound} and {upper_bound}.")
    while True:
        try:
            guess = int(input("Take a guess: "))
        except ValueError:
            print("Invalid input! Please enter a whole number.")
            continue
        if not lower_bound <= guess <= upper_bound:
            print(f"Please enter a number between {lower_bound} and {upper_bound}.")
            continue
        attempts += 1
        if guess < secret_number:
            print("Too low! Try a higher number.")
        elif guess > secret_number:
            print("Too high! Try a lower number.")
        else:
            print(f"Congratulations! You found the secret number after {attempts} valid attempt(s).")
            return

def main():
    while True:
        play_game()
        if input("Would you like to play again? (y/n): ").strip().lower() != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()

"""
USN: 25BTRAD102
LAB EXERCISE 10: FREQUENCY COUNTER USING DICTIONARIES

QUESTION:
Develop a Python program to count the frequency of words in a sentence or
occurrences of elements in a list using dictionaries.

CRITICAL THINKING (CT):
Analyze input data, implement frequency counting, and verify output accuracy.

REAL WORLD EXPOSURE (RWE):
Apply frequency counting to survey responses, classroom feedback, or product
preferences and interpret the findings.
"""

import re


def count_words(sentence):
    words = re.findall(r"\b[\w']+\b", sentence.casefold())
    frequencies = {}
    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies


def count_list_elements(items):
    frequencies = {}
    for item in items:
        frequencies[item] = frequencies.get(item, 0) + 1
    return frequencies


def main():
    while True:
        print("\n--- FREQUENCY COUNTER ---")
        print("1. Count words in a sentence")
        print("2. Count elements in a list")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            sentence = input("Enter a sentence: ").strip()
            if not sentence:
                print("Please enter a non-empty sentence.")
                continue
            result = count_words(sentence)
            print("\nWord frequencies:")
            for word, count in sorted(result.items()):
                print(f"{word}: {count}")

        elif choice == "2":
            raw_items = input("Enter list elements separated by commas: ")
            items = [item.strip() for item in raw_items.split(",") if item.strip()]
            if not items:
                print("Please enter at least one list element.")
                continue
            result = count_list_elements(items)
            print("\nElement frequencies:")
            for item, count in result.items():
                print(f"{item}: {count}")

        elif choice == "3":
            break
        else:
            print("Invalid choice. Enter a number from 1 to 3.")


if __name__ == "__main__":
    main()

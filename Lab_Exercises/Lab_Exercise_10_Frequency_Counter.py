"""Lab Exercise 10: Count word frequencies using a dictionary."""

import re


def count_words(sentence):
    """Return a dictionary of case-insensitive word frequencies."""
    words = re.findall(r"\b[\w']+\b", sentence.casefold())
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


def count_elements(items):
    """Return a dictionary containing the frequency of each list element."""
    frequency = {}
    for item in items:
        frequency[item] = frequency.get(item, 0) + 1
    return frequency


def main():
    sentence = input("Enter a sentence: ")
    frequency = count_words(sentence)

    print("\n--- WORD FREQUENCY ---")
    if not frequency:
        print("No words found.")
    else:
        for word, count in frequency.items():
            print(f"{word}: {count}")

    # Example of counting repeated elements in a list:
    sample_numbers = [10, 20, 10, 30, 20, 10, 40, 30]
    print("\n--- SAMPLE LIST FREQUENCY ---")
    for number, count in count_elements(sample_numbers).items():
        print(f"{number}: {count}")


if __name__ == "__main__":
    main()

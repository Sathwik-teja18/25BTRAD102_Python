# Python Lab Exercises 8-10

This folder contains three menu/input-driven Python practical exercises for lists, dictionaries, loops, functions and conditional statements.

## Files

| Exercise | File | Main concepts |
|---|---|---|
| 8 | [Contact Book](Lab_Exercise_8_Contact_Book.py) | List of dictionaries; add, search, update, delete and display |
| 9 | [Student Grading System](Lab_Exercise_9_Student_Grading_System.py) | Dictionary, validation and if/elif/else grade boundaries |
| 10 | [Frequency Counter](Lab_Exercise_10_Frequency_Counter.py) | Dictionary counting for words and list elements |

## Run

Use Python 3. Run any exercise from a terminal:

```bash
python Lab_Exercise_8_Contact_Book.py
python Lab_Exercise_9_Student_Grading_System.py
python Lab_Exercise_10_Frequency_Counter.py
```

## Exercise 8: Contact Book

A list stores multiple contact dictionaries. Each dictionary contains a name, phone number and email. The program supports adding, searching (case-insensitive), updating, deleting and displaying contacts. Contacts are held in memory for the duration of the program; they are not saved to disk.

**Complexity:** Searching is O(n) in the worst case for n contacts. Appending is amortized O(1).

**Real-world application:** A small personal, college or office contact directory.

## Exercise 9: Student Grading System

A dictionary maps each student name to marks. Marks are validated to be between 0 and 100 before a grade is assigned.

| Marks | Grade |
|---:|---|
| 90-100 | A+ |
| 80-89.99 | A |
| 70-79.99 | B |
| 60-69.99 | C |
| 50-59.99 | D |
| 0-49.99 | F |

**Boundary checks:** 90 -> A+, 89 -> A, 80 -> A, 79 -> B, 70 -> B, 69 -> C, 60 -> C, 59 -> D, 50 -> D, 49 -> F, 0 -> F, 100 -> A+.

**Real-world application:** A basic academic result processing system. A production system would normally use student IDs so duplicate names are not overwritten.

## Exercise 10: Frequency Counter

The program counts case-insensitive words in a sentence and also demonstrates counting repeated list elements. Punctuation is ignored when tokenizing words.

**Complexity:** O(n) average time for n words/elements, using dictionary lookups and updates.

**Real-world application:** Summarizing survey responses, classroom feedback or product preferences.

## Critical Thinking (CT) and Real World Exposure (RWE)

- **CT:** Select suitable data structures, break the problem into functions, validate input, consider boundary cases and reason about time complexity.
- **RWE:** Apply the structures to contact management, academic assessment and survey/text analysis.

## Notes

These are educational command-line examples. Data is not persisted between runs, and the grading scale is an illustrative scale that should be changed to match the institution's official rules.

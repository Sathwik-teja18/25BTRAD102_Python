"""
USN: 25BTRAD102
LAB EXERCISE 15: LIBRARY MANAGEMENT SYSTEM

QUESTION:
Develop a Python program using classes and objects to manage books, issue
and return books, and maintain availability status.

CRITICAL THINKING (CT):
Identify suitable classes and attributes, implement methods, apply
inheritance where appropriate, and test book availability and issue/return
conditions.

REAL WORLD EXPOSURE (RWE):
Simulate library operations and demonstrate how the system supports book
tracking and efficient resource management.
"""


class LibraryItem:
    def __init__(self, title, item_id):
        self.title = title
        self.item_id = item_id
        self.is_available = True

    def issue(self):
        if not self.is_available:
            print(f'"{self.title}" is already issued.')
            return False
        self.is_available = False
        print(f'"{self.title}" has been issued.')
        return True

    def return_item(self):
        if self.is_available:
            print(f'"{self.title}" was not issued.')
            return False
        self.is_available = True
        print(f'"{self.title}" has been returned.')
        return True


class Book(LibraryItem):
    def __init__(self, title, item_id, author):
        super().__init__(title, item_id)
        self.author = author

    def display(self):
        status = "Available" if self.is_available else "Issued"
        print(
            f"ID: {self.item_id} | Title: {self.title} | "
            f"Author: {self.author} | Status: {status}"
        )


class Library:
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        if book.item_id in self.books:
            print("A book with this ID already exists.")
            return
        self.books[book.item_id] = book
        print("Book added.")

    def issue_book(self, item_id):
        book = self.books.get(item_id)
        if book:
            book.issue()
        else:
            print("Book ID not found.")

    def return_book(self, item_id):
        book = self.books.get(item_id)
        if book:
            book.return_item()
        else:
            print("Book ID not found.")

    def display_books(self):
        if not self.books:
            print("No books in the library.")
            return
        for book in self.books.values():
            book.display()


def main():
    library = Library()

    while True:
        print("\n--- LIBRARY MANAGEMENT SYSTEM ---")
        print("1. Add book")
        print("2. Issue book")
        print("3. Return book")
        print("4. Display books")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            item_id = input("Enter book ID: ").strip()
            title = input("Enter book title: ").strip()
            author = input("Enter author: ").strip()
            if not all((item_id, title, author)):
                print("All book details are required.")
            else:
                library.add_book(Book(title, item_id, author))
        elif choice == "2":
            library.issue_book(input("Enter book ID to issue: ").strip())
        elif choice == "3":
            library.return_book(input("Enter book ID to return: ").strip())
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()

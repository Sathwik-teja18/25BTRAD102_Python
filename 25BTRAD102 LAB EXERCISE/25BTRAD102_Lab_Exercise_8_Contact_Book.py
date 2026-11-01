"""
USN: 25BTRAD102
LAB EXERCISE 8: CONTACT BOOK USING LISTS AND DICTIONARIES

QUESTION:
Develop a Python program to add, search, update, delete, and display
contact details using lists and dictionaries.

CRITICAL THINKING (CT):
Analyze requirements, select suitable data structures, implement operations,
and test correctness.

REAL WORLD EXPOSURE (RWE):
Apply the contact book to a personal or organizational contact-management
scenario.
"""

contacts = []


def find_contact(name):
    for contact in contacts:
        if contact["name"].casefold() == name.casefold():
            return contact
    return None


def add_contact():
    name = input("Enter name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    if find_contact(name):
        print("A contact with this name already exists.")
        return

    phone = input("Enter phone number: ").strip()
    email = input("Enter email address: ").strip()
    contacts.append({"name": name, "phone": phone, "email": email})
    print("Contact added.")


def search_contact():
    name = input("Enter the name to search: ").strip()
    contact = find_contact(name)
    if contact:
        print(f'Name: {contact["name"]}')
        print(f'Phone: {contact["phone"]}')
        print(f'Email: {contact["email"]}')
    else:
        print("Contact not found.")


def update_contact():
    name = input("Enter the name to update: ").strip()
    contact = find_contact(name)
    if not contact:
        print("Contact not found.")
        return

    phone = input("Enter new phone number (leave blank to keep current): ").strip()
    email = input("Enter new email (leave blank to keep current): ").strip()
    if phone:
        contact["phone"] = phone
    if email:
        contact["email"] = email
    print("Contact updated.")


def delete_contact():
    name = input("Enter the name to delete: ").strip()
    contact = find_contact(name)
    if contact:
        contacts.remove(contact)
        print("Contact deleted.")
    else:
        print("Contact not found.")


def display_contacts():
    if not contacts:
        print("The contact book is empty.")
        return

    print("\nCONTACT LIST")
    for number, contact in enumerate(contacts, start=1):
        print(
            f'{number}. {contact["name"]} | '
            f'Phone: {contact["phone"]} | Email: {contact["email"]}'
        )


def main():
    while True:
        print("\n--- CONTACT BOOK ---")
        print("1. Add contact")
        print("2. Search contact")
        print("3. Update contact")
        print("4. Delete contact")
        print("5. Display all contacts")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contact()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            display_contacts()
        elif choice == "6":
            print("Exiting contact book.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()

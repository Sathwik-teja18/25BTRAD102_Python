"""Lab Exercise 8: Contact Book using lists and dictionaries."""

contacts = []


def find_contact(name):
    """Return the first contact matching name, ignoring case."""
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
        print("A contact with that name already exists.")
        return

    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()
    contacts.append({"name": name, "phone": phone, "email": email})
    print("Contact added successfully!")


def search_contact():
    name = input("Enter name to search: ").strip()
    contact = find_contact(name)
    if contact:
        print("Contact found:")
        print(f"Name: {contact['name']} | Phone: {contact['phone']} | Email: {contact['email']}")
    else:
        print("Contact not found.")


def update_contact():
    name = input("Enter name to update: ").strip()
    contact = find_contact(name)
    if not contact:
        print("Contact not found.")
        return

    new_phone = input(f"New phone [{contact['phone']}]: ").strip()
    new_email = input(f"New email [{contact['email']}]: ").strip()
    if new_phone:
        contact["phone"] = new_phone
    if new_email:
        contact["email"] = new_email
    print("Contact updated successfully!")


def delete_contact():
    name = input("Enter name to delete: ").strip()
    contact = find_contact(name)
    if contact:
        contacts.remove(contact)
        print("Contact deleted successfully!")
    else:
        print("Contact not found.")


def display_contacts():
    if not contacts:
        print("No contacts available.")
        return
    print("\\n--- SAVED CONTACTS ---")
    for contact in contacts:
        print(f"{contact['name']} | {contact['phone']} | {contact['email']}")


def main():
    while True:
        print("\\n--- CONTACT BOOK ---")
        print("1. Add Contact\\n2. Search Contact\\n3. Update Contact")
        print("4. Delete Contact\\n5. Display Contacts\\n6. Exit")
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
            print("Exiting Contact Book.")
            break
        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()

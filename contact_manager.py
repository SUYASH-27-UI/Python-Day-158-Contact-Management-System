
import csv
import os

FILE_NAME = "contacts.csv"

FIELDS = ["id", "name", "phone", "email"]


def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", newline="") as file:
            return list(csv.DictReader(file))
    except (OSError, csv.Error):
        print("Error reading contacts file.")
        return []


def save_contacts(contacts):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(contacts)


def generate_id(contacts):
    ids = [int(c["id"]) for c in contacts if c["id"].isdigit()]
    return max(ids, default=1000) + 1


def add_contact(contacts):
    name = input("Enter Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email: ").strip()

    if not name or not phone or not email:
        print("All fields are required!")
        return

    if not phone.isdigit() or len(phone) < 7:
        print("Enter a valid phone number!")
        return

    if any(c["phone"] == phone for c in contacts):
        print("Phone number already exists!")
        return

    contact = {
        "id": str(generate_id(contacts)),
        "name": name,
        "phone": phone,
        "email": email
    }

    contacts.append(contact)
    save_contacts(contacts)
    print("Contact added successfully!")
    print("Contact ID:", contact["id"])


def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    print("\n===== ALL CONTACTS =====")

    for c in contacts:
        print(
            f'ID: {c["id"]} | Name: {c["name"]} | '
            f'Phone: {c["phone"]} | Email: {c["email"]}'
        )


def search_contact(contacts):
    keyword = input("Enter Name or Phone: ").strip().lower()

    results = [
        c for c in contacts
        if keyword in c["name"].lower()
        or keyword in c["phone"].lower()
    ]

    if results:
        for c in results:
            print(c)
    else:
        print("Contact not found.")


def update_contact(contacts):
    contact_id = input("Enter Contact ID to update: ").strip()

    for c in contacts:
        if c["id"] == contact_id:
            print("Leave a field blank to keep its current value.")

            name = input(f'New Name ({c["name"]}): ').strip()
            phone = input(f'New Phone ({c["phone"]}): ').strip()
            email = input(f'New Email ({c["email"]}): ').strip()

            if phone:
                if not phone.isdigit() or len(phone) < 7:
                    print("Invalid phone number!")
                    return

                if any(
                    other["phone"] == phone and other["id"] != contact_id
                    for other in contacts
                ):
                    print("Phone number already belongs to another contact!")
                    return

            if name:
                c["name"] = name
            if phone:
                c["phone"] = phone
            if email:
                c["email"] = email

            save_contacts(contacts)
            print("Contact updated successfully!")
            return

    print("Contact ID not found.")


def delete_contact(contacts):
    contact_id = input("Enter Contact ID to delete: ").strip()

    for c in contacts:
        if c["id"] == contact_id:
            contacts.remove(c)
            save_contacts(contacts)
            print("Contact deleted successfully!")
            return

    print("Contact ID not found.")


def main():
    contacts = load_contacts()

    while True:
        print("\n===== CONTACT MANAGEMENT SYSTEM =====")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter Choice: ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("Contact Manager Closed.")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()

"""
main.py

This is the file you run to start the program. It shows menus,
reads what the user types, and calls the right function from
services.py to actually do it.
"""

import database
import services
import validation


def member_menu():
    """The submenu for managing members."""
    while True:
        print("\n--- Manage Members ---")
        print("1. Register new member")
        print("2. View all members")
        print("3. Update a member")
        print("4. Delete a member")
        print("5. Back to main menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = validation.ask_for_name("Enter member's full name: ")
            email = validation.ask_for_email("Enter member's email: ")
            member = services.register_member(name, email)
            print("Member registered with ID " + str(member.id) + ".")

        elif choice == "2":
            members = services.list_members()
            if len(members) == 0:
                print("No members yet.")
            else:
                for member in members:
                    print(member.display())

        elif choice == "3":
            member_id = validation.ask_for_a_number("Enter the member ID to update: ")
            name = validation.ask_for_text("Enter the new name: ")
            email = validation.ask_for_email("Enter the new email: ")
            services.update_member(member_id, name, email)
            print("Member updated.")

        elif choice == "4":
            member_id = validation.ask_for_a_number("Enter the member ID to delete: ")
            services.delete_member(member_id)
            print("Member deleted.")

        elif choice == "5":
            return

        else:
            print("Please enter a number from 1 to 5.")


def equipment_menu():
    """The submenu for managing equipment."""
    while True:
        print("\n--- Manage Equipment ---")
        print("1. Register new equipment")
        print("2. View all equipment")
        print("3. Update equipment")
        print("4. Delete equipment")
        print("5. Back to main menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = validation.ask_for_text("Enter equipment name: ")
            category = validation.ask_for_text("Enter equipment category: ")
            equipment = services.register_equipment(name, category)
            print("Equipment registered with ID " + str(equipment.id) + ".")

        elif choice == "2":
            equipment_list = services.list_equipment()
            if len(equipment_list) == 0:
                print("No equipment yet.")
            else:
                for item in equipment_list:
                    print(item.display())

        elif choice == "3":
            equipment_id = validation.ask_for_a_number("Enter the equipment ID to update: ")
            name = validation.ask_for_text("Enter the new name: ")
            category = validation.ask_for_text("Enter the new category: ")
            is_available = validation.ask_for_yes_no("Is it currently available? (Y/N): ")
            services.update_equipment(equipment_id, name, category, is_available)
            print("Equipment updated.")

        elif choice == "4":
            equipment_id = validation.ask_for_a_number("Enter the equipment ID to delete: ")
            services.delete_equipment(equipment_id)
            print("Equipment deleted.")

        elif choice == "5":
            return

        else:
            print("Please enter a number from 1 to 5.")


def checkout_flow():
    """Check out a piece of equipment to a member."""
    print("\n--- Checkout Equipment ---")
    member_id = validation.ask_for_a_number("Enter member ID: ")
    equipment_id = validation.ask_for_a_number("Enter equipment ID: ")
    loan_days = validation.ask_for_a_number("How many days is the loan for? ")

    new_loan_id, message = services.checkout_equipment(member_id, equipment_id, loan_days)
    print(message)


def return_flow():
    """Return a piece of equipment and close its loan."""
    print("\n--- Return Equipment ---")
    print("Active loans:")
    active_loans = services.report_currently_borrowed()
    if len(active_loans) == 0:
        print("No equipment is currently borrowed.")
        return

    for loan in active_loans:
        print("Loan ID " + str(loan["id"]) + ": " + loan["member_name"] +
              " has " + loan["equipment_name"] + " (due " + loan["due_date"] + ")")

    loan_id = validation.ask_for_a_number("Enter the loan ID to return: ")
    message = services.return_equipment(loan_id)
    print(message)


def search_menu():
    """The submenu for searching members and equipment."""
    print("\n--- Search ---")
    print("1. Search members")
    print("2. Search equipment")
    print("3. Back to main menu")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        keyword = validation.ask_for_text("Enter a name to search for: ")
        results = services.search_members(keyword)
        if len(results) == 0:
            print("No members matched.")
        else:
            for member in results:
                print(member.display())

    elif choice == "2":
        keyword = validation.ask_for_text("Enter equipment name to search for: ")
        results = services.search_equipment(keyword)
        if len(results) == 0:
            print("No equipment matched.")
        else:
            for item in results:
                print(item.display())

    elif choice == "3":
        return

    else:
        print("Please enter a number from 1 to 3.")


def reports_menu():
    """The submenu for viewing reports."""
    print("\n--- Reports ---")
    print("1. Currently borrowed equipment")
    print("2. Overdue loans")
    print("3. Equipment by category")
    print("4. Back to main menu")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        loans = services.report_currently_borrowed()
        if len(loans) == 0:
            print("Nothing is currently borrowed.")
        else:
            for loan in loans:
                print(loan["member_name"] + " has " + loan["equipment_name"] +
                      " (due " + loan["due_date"] + ")")

    elif choice == "2":
        loans = services.report_overdue()
        if len(loans) == 0:
            print("No overdue loans.")
        else:
            for loan in loans:
                print(loan["member_name"] + " has " + loan["equipment_name"] +
                      " (was due " + loan["due_date"] + ")")

    elif choice == "3":
        rows = services.report_equipment_by_category()
        if len(rows) == 0:
            print("No equipment yet.")
        else:
            for row in rows:
                print(row["category"] + ": " + str(row["available_items"]) +
                      " available out of " + str(row["total_items"]))

    elif choice == "4":
        return

    else:
        print("Please enter a number from 1 to 4.")


def main():
    """The main menu loop."""
    # Make sure the database file and its tables exist before we
    # try to use them - safe to run every time the program starts.
    database.create_tables()

    print("==========================================")
    print(" CAMPUS MAKERSPACE CHECKOUT SYSTEM")
    print("==========================================")

    program_is_running = True

    while program_is_running:
        print("\n1. Manage Members")
        print("2. Manage Equipment")
        print("3. Checkout Equipment")
        print("4. Return Equipment")
        print("5. Search")
        print("6. Reports")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            member_menu()
        elif choice == "2":
            equipment_menu()
        elif choice == "3":
            checkout_flow()
        elif choice == "4":
            return_flow()
        elif choice == "5":
            search_menu()
        elif choice == "6":
            reports_menu()
        elif choice == "7":
            print("Goodbye!")
            program_is_running = False
        else:
            print("Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()

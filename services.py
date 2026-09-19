"""
services.py

This file connects models.py and database.py together. It holds
our "real world actions" - things like "register a new member" or
"check out a piece of equipment" - and coordinates both files to
make that happen correctly.
"""

import datetime
import database
import models


def today_text():
    """Get today's date as plain text, like '2026-09-08'."""
    return str(datetime.date.today())


# -----------------------------------------------------------------
# MEMBERS
# -----------------------------------------------------------------

def register_member(name, email):
    """Save a new member, then return a real Member object."""
    new_id = database.insert_member(name, email)
    return models.Member(name, email, new_id)


def list_members():
    """Return every saved member as a list of real Member objects."""
    rows = database.get_all_members()
    members = []
    for row in rows:
        members.append(models.Member.from_row(row))
    return members


def update_member(member_id, name, email):
    """Change an existing member's details."""
    database.update_member(member_id, name, email)


def delete_member(member_id):
    """Remove a member permanently."""
    database.delete_member(member_id)


def search_members(keyword):
    """Find members whose name contains this keyword."""
    rows = database.search_members(keyword)
    members = []
    for row in rows:
        members.append(models.Member.from_row(row))
    return members


# -----------------------------------------------------------------
# EQUIPMENT
# -----------------------------------------------------------------

def register_equipment(name, category):
    """Save new equipment, then return a real Equipment object."""
    new_id = database.insert_equipment(name, category)
    return models.Equipment(name, category, True, new_id)


def list_equipment():
    """Return every saved item as a list of real Equipment objects."""
    rows = database.get_all_equipment()
    equipment_list = []
    for row in rows:
        equipment_list.append(models.Equipment.from_row(row))
    return equipment_list


def update_equipment(equipment_id, name, category, is_available):
    """Change an existing equipment item's details."""
    if is_available:
        available_value = 1
    else:
        available_value = 0
    database.update_equipment(equipment_id, name, category, available_value)


def delete_equipment(equipment_id):
    """Remove an equipment item permanently."""
    database.delete_equipment(equipment_id)


def search_equipment(keyword):
    """Find equipment whose name contains this keyword."""
    rows = database.search_equipment(keyword)
    equipment_list = []
    for row in rows:
        equipment_list.append(models.Equipment.from_row(row))
    return equipment_list


# -----------------------------------------------------------------
# CHECKOUT AND RETURN (this is where Member, Equipment, and Loan
# objects all work together - our "object collaboration")
# -----------------------------------------------------------------

def checkout_equipment(member_id, equipment_id, loan_days):
    """
    Try to check out a piece of equipment to a member.
    Returns (new_loan_id, message). new_loan_id is None if it failed.
    """
    member_row = database.get_member_by_id(member_id)
    if member_row is None:
        return None, "No member found with that ID."

    equipment_row = database.get_equipment_by_id(equipment_id)
    if equipment_row is None:
        return None, "No equipment found with that ID."

    # Turn the row into a real object so we can use its methods.
    equipment = models.Equipment.from_row(equipment_row)
    if not equipment.is_available:
        return None, "This equipment is already borrowed."

    checkout_date = datetime.date.today()
    due_date = checkout_date + datetime.timedelta(days=loan_days)
    checkout_date_text = str(checkout_date)
    due_date_text = str(due_date)

    new_loan_id = database.insert_loan(member_id, equipment_id, checkout_date_text, due_date_text)

    # Update the object's own state, then save that change.
    equipment.mark_borrowed()
    database.update_equipment(equipment_id, equipment.name, equipment.category, 0)

    return new_loan_id, "Checked out successfully. Due back " + due_date_text + "."


def return_equipment(loan_id):
    """Close a loan and mark its equipment as available again."""
    loan_row = database.get_loan_by_id(loan_id)
    if loan_row is None:
        return "No loan found with that ID."

    loan = models.Loan.from_row(loan_row)
    if loan.status == "returned":
        return "This loan has already been returned."

    return_date_text = today_text()
    loan.close(return_date_text)
    database.close_loan(loan_id, return_date_text)

    equipment_row = database.get_equipment_by_id(loan.equipment_id)
    equipment = models.Equipment.from_row(equipment_row)
    equipment.mark_returned()
    database.update_equipment(loan.equipment_id, equipment.name, equipment.category, 1)

    return "Equipment returned successfully."


# -----------------------------------------------------------------
# REPORTS
# -----------------------------------------------------------------

def report_currently_borrowed():
    """Every loan that has not been returned yet."""
    return database.get_active_loans()


def report_overdue():
    """Every active loan whose due date has already passed."""
    return database.get_overdue_loans(today_text())


def report_equipment_by_category():
    """A count of equipment in each category, and how many are free."""
    return database.get_equipment_by_category_report()

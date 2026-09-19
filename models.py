"""
models.py

This file has our three classes: Member, Equipment, and Loan.

A CLASS is a blueprint. An OBJECT is one real thing made from that
blueprint. For example, Member is the blueprint for "a person who
can borrow things" - every time someone registers, we create one
Member object using that blueprint.

Each class has:
  - attributes: information it holds (like a name, or a date)
  - methods: things it can do (like "mark this as borrowed")
"""


class Member:
    """A person who can borrow equipment."""

    def __init__(self, name, email, id=None):
        # "self" means "this specific object". Every Member object
        # gets its own name, email, and id, stored on itself.
        self.id = id
        self.name = name
        self.email = email

    @classmethod
    def from_row(cls, row):
        """
        Build a Member object out of one row we got back from the
        database. This is how database data becomes a real object
        we can work with in Python.
        """
        return cls(row["name"], row["email"], row["id"])

    def display(self):
        """Return a neat, readable line describing this member."""
        return "ID " + str(self.id) + ": " + self.name + " (" + self.email + ")"


class Equipment:
    """One item that members can borrow (camera, laptop, etc.)."""

    def __init__(self, name, category, is_available=True, id=None):
        self.id = id
        self.name = name
        self.category = category
        # In Python we use True/False. The database stores this as
        # 1/0 instead, since SQLite has no true/false type of its own.
        self.is_available = is_available

    @classmethod
    def from_row(cls, row):
        """Build an Equipment object out of one database row."""
        available = (row["is_available"] == 1)
        return cls(row["name"], row["category"], available, row["id"])

    def mark_borrowed(self):
        """Change this equipment's own state to 'not available'."""
        self.is_available = False

    def mark_returned(self):
        """Change this equipment's own state back to 'available'."""
        self.is_available = True

    def display(self):
        """Return a neat, readable line describing this equipment."""
        if self.is_available:
            status_text = "Available"
        else:
            status_text = "Borrowed"
        return "ID " + str(self.id) + ": " + self.name + " (" + self.category + ") - " + status_text


class Loan:
    """One record of a member borrowing one piece of equipment."""

    def __init__(self, member_id, equipment_id, checkout_date, due_date, return_date=None, status="active", id=None):
        self.id = id
        self.member_id = member_id
        self.equipment_id = equipment_id
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status

    @classmethod
    def from_row(cls, row):
        """Build a Loan object out of one database row."""
        return cls(
            row["member_id"],
            row["equipment_id"],
            row["checkout_date"],
            row["due_date"],
            row["return_date"],
            row["status"],
            row["id"]
        )

    def is_overdue(self, today_text):
        """
        Check if this loan is overdue: it must still be active
        (not yet returned), AND its due date must already be in
        the past compared to today.
        """
        if self.status == "active" and self.due_date < today_text:
            return True
        else:
            return False

    def close(self, return_date):
        """Mark this loan's own state as finished/returned."""
        self.return_date = return_date
        self.status = "returned"

    def display(self):
        """Return a neat, readable line describing this loan."""
        return ("Loan ID " + str(self.id) + ": Member " + str(self.member_id) +
                " borrowed Equipment " + str(self.equipment_id) +
                " (due " + self.due_date + ", status: " + self.status + ")")

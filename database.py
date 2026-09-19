"""
database.py

This file is the ONLY file that talks directly to our SQLite
database. Everywhere else in the program, if something needs to be
saved, looked up, changed, or removed, it asks THIS file to do it.

A database is like a set of spreadsheets stored in one file. Each
"table" below is like one spreadsheet, with rows and columns.
"""

import sqlite3

# This is the name of our database file. SQLite will create this
# file automatically the very first time we run the program.
DB_FILE = "makerspace.db"


def get_connection():
    """
    Open a connection to our database file. Think of this as
    "unlocking" the file so we can read from it or write to it.
    Every function below calls this first.
    """
    connection = sqlite3.connect(DB_FILE)
    # This makes rows come back as dictionaries (with column names),
    # instead of plain unlabeled lists of values - much easier to read.
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    """
    Create our three tables, if they do not already exist.
    This is safe to run every time the program starts - if the
    tables are already there, nothing happens.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # The members table: one row per person who can borrow equipment.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT
        )
    """)

    # The equipment table: one row per item that can be borrowed.
    # is_available is stored as 1 (yes) or 0 (no), since SQLite has
    # no true/false type of its own.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            is_available INTEGER NOT NULL DEFAULT 1
        )
    """)

    # The loans table: one row every time someone borrows something.
    # member_id and equipment_id are not the full member or equipment
    # details - just their ID numbers, pointing back to the other two
    # tables. This avoids storing the same name/email over and over.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            equipment_id INTEGER NOT NULL,
            checkout_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            FOREIGN KEY (member_id) REFERENCES members (id),
            FOREIGN KEY (equipment_id) REFERENCES equipment (id)
        )
    """)

    # Nothing is actually saved to the file until we "commit" -
    # think of this as pressing Save.
    connection.commit()
    connection.close()


# -----------------------------------------------------------------
# MEMBERS: Create, Read, Update, Delete
# -----------------------------------------------------------------

def insert_member(name, email):
    """Add a new member. Returns the new member's ID number."""
    connection = get_connection()
    cursor = connection.cursor()
    # The "?" marks are placeholders. SQLite safely fills them in
    # with our actual values - this protects us from a common
    # security problem called "SQL injection".
    cursor.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
    connection.commit()
    new_id = cursor.lastrowid  # the ID SQLite just gave this new row
    connection.close()
    return new_id


def get_all_members():
    """Return every member as a list of rows."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM members ORDER BY id")
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_member_by_id(member_id):
    """Return one member's row, or None if no member has this ID."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
    row = cursor.fetchone()
    connection.close()
    return row


def update_member(member_id, name, email):
    """Change an existing member's name and email."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE members SET name = ?, email = ? WHERE id = ?", (name, email, member_id))
    connection.commit()
    connection.close()


def delete_member(member_id):
    """Remove a member permanently."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
    connection.commit()
    connection.close()


def search_members(keyword):
    """Find members whose name contains this keyword."""
    connection = get_connection()
    cursor = connection.cursor()
    # The % signs mean "anything can come before or after" the keyword.
    cursor.execute("SELECT * FROM members WHERE name LIKE ?", ("%" + keyword + "%",))
    rows = cursor.fetchall()
    connection.close()
    return rows


# -----------------------------------------------------------------
# EQUIPMENT: Create, Read, Update, Delete
# -----------------------------------------------------------------

def insert_equipment(name, category):
    """Add a new piece of equipment. New equipment starts as available."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO equipment (name, category, is_available) VALUES (?, ?, 1)", (name, category))
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return new_id


def get_all_equipment():
    """Return every piece of equipment as a list of rows."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM equipment ORDER BY id")
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_equipment_by_id(equipment_id):
    """Return one piece of equipment's row, or None if not found."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM equipment WHERE id = ?", (equipment_id,))
    row = cursor.fetchone()
    connection.close()
    return row


def update_equipment(equipment_id, name, category, is_available):
    """Change an existing piece of equipment's details."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE equipment SET name = ?, category = ?, is_available = ? WHERE id = ?",
        (name, category, is_available, equipment_id)
    )
    connection.commit()
    connection.close()


def delete_equipment(equipment_id):
    """Remove a piece of equipment permanently."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM equipment WHERE id = ?", (equipment_id,))
    connection.commit()
    connection.close()


def search_equipment(keyword):
    """Find equipment whose name contains this keyword."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM equipment WHERE name LIKE ?", ("%" + keyword + "%",))
    rows = cursor.fetchall()
    connection.close()
    return rows


# -----------------------------------------------------------------
# LOANS: Create, Read, Update (closing a loan)
# -----------------------------------------------------------------

def insert_loan(member_id, equipment_id, checkout_date, due_date):
    """Create a new loan (a checkout). Returns the new loan's ID."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO loans (member_id, equipment_id, checkout_date, due_date, status) VALUES (?, ?, ?, ?, 'active')",
        (member_id, equipment_id, checkout_date, due_date)
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return new_id


def get_loan_by_id(loan_id):
    """Return one loan's row, or None if not found."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM loans WHERE id = ?", (loan_id,))
    row = cursor.fetchone()
    connection.close()
    return row


def close_loan(loan_id, return_date):
    """Mark a loan as returned, and record the return date."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE loans SET return_date = ?, status = 'returned' WHERE id = ?",
        (return_date, loan_id)
    )
    connection.commit()
    connection.close()


def get_active_loans():
    """
    Return every loan that has not been returned yet, joined with
    the member's name and the equipment's name (so we do not have
    to look those up separately).
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT loans.id, loans.checkout_date, loans.due_date,
               members.name AS member_name,
               equipment.name AS equipment_name
        FROM loans
        JOIN members ON loans.member_id = members.id
        JOIN equipment ON loans.equipment_id = equipment.id
        WHERE loans.status = 'active'
        ORDER BY loans.due_date
    """)
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_overdue_loans(today_text):
    """
    Return every active loan whose due date has already passed,
    compared to today's date (given to us as text, like "2026-09-08").
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT loans.id, loans.checkout_date, loans.due_date,
               members.name AS member_name,
               equipment.name AS equipment_name
        FROM loans
        JOIN members ON loans.member_id = members.id
        JOIN equipment ON loans.equipment_id = equipment.id
        WHERE loans.status = 'active' AND loans.due_date < ?
        ORDER BY loans.due_date
    """, (today_text,))
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_equipment_by_category_report():
    """
    Return a count of equipment in each category, and how many of
    each are currently available.
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT category,
               COUNT(*) AS total_items,
               SUM(is_available) AS available_items
        FROM equipment
        GROUP BY category
    """)
    rows = cursor.fetchall()
    connection.close()
    return rows

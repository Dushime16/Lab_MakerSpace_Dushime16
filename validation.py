"""
validation.py

This file checks that whatever the user types is safe to use.
Every function here keeps asking again if the answer is bad, so
the program never crashes because of bad input.
"""


def ask_for_text(question):
    """Keep asking until the user types something that is not empty."""
    while True:
        text = input(question)
        text = text.strip()
        if text == "":
            print("This cannot be empty. Please type something.")
        else:
            return text


def ask_for_a_number(question):
    """Keep asking until the user types a whole number bigger than 0."""
    while True:
        text = input(question)
        try:
            number = int(text)
            if number > 0:
                return number
            else:
                print("Please enter a number bigger than 0.")
        except ValueError:
            print("That is not a valid number. Please try again.")


def ask_for_email(question):
    """
    Keep asking until the answer at least looks like an email
    address - contains an @ symbol and a dot, and is not empty.
    This is a simple check, not a perfect one.
    """
    while True:
        email = input(question)
        email = email.strip()
        if email == "":
            print("Email cannot be empty.")
        elif "@" not in email or "." not in email:
            print("Please enter a valid email address (must contain @ and .)")
        else:
            return email


def ask_for_yes_no(question):
    """Keep asking until the user answers yes or no. Returns True or False."""
    while True:
        answer = input(question)
        answer = answer.strip().lower()
        if answer == "y" or answer == "yes":
            return True
        elif answer == "n" or answer == "no":
            return False
        else:
            print("Please type Y for yes or N for no.")

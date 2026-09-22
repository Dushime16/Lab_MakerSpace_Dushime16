# Campus MakerSpace Checkout System

A command-line program that helps a student makerspace keep track
of its equipment, its members, and who currently has what borrowed.

## What it can do

- Add, view, update, and delete members
- Add, view, update, and delete equipment
- Check out equipment to a member (only if it's actually available)
- Return equipment
- Search for a member or a piece of equipment by name
- View 3 reports: what's currently borrowed, what's overdue, and
  equipment counts by category

## Files in this project

- `main.py` — the menu you actually run
- `models.py` — the Member, Equipment, and Loan classes
- `database.py` — saves and loads everything using SQLite
- `services.py` — connects the classes and the database together
- `validation.py` — makes sure nothing typed by the user can crash
  the program
- `requirements.txt` — nothing extra to install, just Python itself
- `.gitignore` — keeps unnecessary system files out of the repo

## The three things we keep track of

**A Member** — someone who can borrow things. Has a name and an email.

**A piece of Equipment** — something that can be borrowed, like a
camera or a laptop. Has a name, a category, and whether it's
currently available.

**A Loan** — one record of someone borrowing something. Tracks who
borrowed it, what they borrowed, when, when it's due back, and
whether it's been returned yet.

## How the data is stored

Everything is saved in one file, `makerspace.db`, split into three
tables:

**members**
| Column | Holds |
|---|---|
| id | a number |
| name | text |
| email | text |

**equipment**
| Column | Holds |
|---|---|
| id | a number |
| name | text |
| category | text |
| is_available | a number (1 = yes, 0 = no) |

**loans**
| Column | Holds |
|---|---|
| id | a number |
| member_id | a number (points to someone in the members table) |
| equipment_id | a number (points to something in the equipment table) |
| checkout_date | text |
| due_date | text |
| return_date | text (empty until it's returned) |
| status | text ("active" or "returned") |

The loans table only stores ID numbers for who borrowed what, not
their full details again - that way we're not storing the same
name over and over. When we need to show a name in a report, we
look it back up using those ID numbers.

## How to run it

1. Make sure all the files are in the same folder.
2. Open a terminal in that folder.
3. Run:

```
python3 main.py
```

The database file gets created automatically the first time you
run it, and everything you add stays saved for next time.

## AI Assistance

Claude (Anthropic) was used as a learning aid to explain OOP and
SQLite concepts, and to help design and debug.

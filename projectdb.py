import sqlite3
from datetime import datetime

contacts_db = sqlite3.connect(r"database/contacts.db")
reminders_db = sqlite3.connect(r"database/reminders.db")


def insert_contact_db(name, number):
    # create cursor object to send sql commands to contacts_db
    cursor = contacts_db.cursor()
    cursor.execute("INSERT INTO contacts VALUES (?, ?)", (name, number))
    contacts_db.commit()


def read_contact_db(name):
    cursor = contacts_db.cursor()
    number_command = cursor.execute(f"SELECT * FROM contacts WHERE name = '{name}'")
    for column in number_command:
        number = column[1]
        print(number)
        return number


def insert_reminder_db(reminder_time, reminder_text):
    cursor = reminders_db.cursor()
    cursor.execute(
        "INSERT INTO reminders (reminder_time, reminder_text) VALUES (?, ?)",
        (reminder_time, reminder_text),
    )
    reminders_db.commit()


def read_reminder_db():
    cursor = reminders_db.cursor()
    cursor.execute("SELECT reminder_time, reminder_text FROM reminders")
    columns = cursor.fetchall()
    return columns


def insertnowtime():
    motiondetect_db = sqlite3.connect(r"database/motiondetect.db")
    cursor_obj = motiondetect_db.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # Insert the current time into the database
    cursor_obj.execute(f"INSERT INTO LastActiveTime (Time) VALUES (?)", (now,))
    motiondetect_db.commit()


def is_table_empty():
    motiondetect_db = sqlite3.connect(r"database/motiondetect.db")
    cursor_obj = motiondetect_db.cursor()

    # Execute a query to count the number of rows in the table
    cursor_obj.execute(f"SELECT COUNT(*) FROM LastActiveTime")
    row_count = cursor_obj.fetchone()[0]
    if row_count == 0:
        return True
    else:
        return False


def cleanOldEntries(timepast):
    motiondetect_db = sqlite3.connect(r"database/motiondetect.db")
    cursor_obj = motiondetect_db.cursor()
    cursor_obj.execute("DELETE FROM LastActiveTime WHERE Time != ?", (timepast,))
    motiondetect_db.commit()


def selectNewestTime():
    motiondetect_db = sqlite3.connect(r"database/motiondetect.db")
    cursor_obj = motiondetect_db.cursor()
    cursor_obj.execute("""SELECT * FROM LastActiveTime order by Time desc Limit 1""")
    output = cursor_obj.fetchall()
    return output
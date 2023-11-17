import sqlite3

contacts_db = sqlite3.connect(r"/home/afiq/database/contacts.db")
reminders_db = sqlite3.connect(r"/home/afiq/database/reminders.db")

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
    cursor.execute("INSERT INTO reminders (reminder_time, reminder_text) VALUES (?, ?)", (reminder_time, reminder_text))
    reminders_db.commit()
    
def read_reminder_db():
    cursor = reminders_db.cursor()
    cursor.execute("SELECT reminder_time, reminder_text FROM reminders")
    columns = cursor.fetchall()
    return columns
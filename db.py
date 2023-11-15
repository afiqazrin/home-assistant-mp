import sqlite3

contacts_db = sqlite3.connect(r"/home/afiq/contacts.db")


def insert_contact_db(name, number):
    # create cursor object to send sql commands to contacts_db
    cursor = contacts_db.cursor()
    cursor.execute("INSERT INTO contacts VALUES (?, ?)", (name, number))

def read_contact_db(name):
    cursor = contacts_db.cursor()
    number_command = cursor.execute(f"SELECT * FROM contacts WHERE name = '{name}'")
    for column in number_command: 
        number = column[1]
        print(number)
        return number
    
contacts_db.commit()


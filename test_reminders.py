import schedule
import time
from dateutil import parser
import sqlite3

def connect_to_database(database_name=('/home/afiq/database/reminders.db')):
    """Connect to the SQLite database and return the connection and cursor."""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    return conn, cursor

def create_reminders_table(cursor):
    """Create the reminders table if it doesn't exist."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, reminder_time TEXT, reminder_text TEXT)''')

def insert_reminder(cursor, conn, reminder_time, reminder_text):
    """Insert a reminder into the database."""
    cursor.execute("INSERT INTO reminders (reminder_time, reminder_text) VALUES (?, ?)", (reminder_time, reminder_text))
    conn.commit()

def reminder_callback(reminder_text, reminder_time):
    """Callback function when the reminder triggers."""
    print(f"Reminder: {reminder_text}")
    time.sleep(2)  # Wait for 2 seconds between reminders

def schedule_reminders(reminder_time, reminder_text):
    """Schedule a reminder to ring twice at the specified time."""
    schedule.every().day.at(reminder_time.strftime('%H:%M')).do(
        reminder_callback, reminder_text, reminder_time
    ).tag('reminder').tag('first')
    schedule.every().day.at(reminder_time.strftime('%H:%M')).do(
        reminder_callback, reminder_text, reminder_time
    ).tag('reminder').tag('second')

def get_user_input(cursor, conn):
    """Get user input for reminders and return the list of reminders."""
    total_reminders = 0

    # Retrieve existing reminders from the database
    cursor.execute("SELECT reminder_time, reminder_text FROM reminders")
    rows = cursor.fetchall()

    current_time = parser.parse(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    for row in rows:
        reminder_time, reminder_text = row
        parsed_time = parser.parse(reminder_time)
        if parsed_time > current_time:
            insert_reminder(cursor, conn, parsed_time, reminder_text)
            total_reminders += 1

    while True:
        num_reminders = int(input("How many reminders do you want to set (0 to exit)? "))
        if num_reminders == 0:
            break

        for i in range(num_reminders):
            reminder_text = input(f"Enter reminder {total_reminders + 1} message: ")
            reminder_time = input(f"Enter reminder {total_reminders + 1} time (e.g., '1 November at 3:30 PM'): ")
            parsed_time = parser.parse(reminder_time)
            
            # Check if the reminder time is in the future
            if parsed_time > current_time:
                insert_reminder(cursor, conn, parsed_time, reminder_text)
                total_reminders += 1
            else:
                print("Reminder time has already passed. Please enter a future time.")

        set_another = input("Do you want to set another reminder? (yes/no): ").lower()
        if set_another != 'yes':
            break

    # Return is not needed as you are using a global connection and cursor

def main():
    global conn, cursor
    conn, cursor = connect_to_database()
    create_reminders_table(cursor)

    get_user_input(cursor, conn)

    cursor.execute("SELECT reminder_time, reminder_text FROM reminders")
    rows = cursor.fetchall()

    for row in rows:
        reminder_time, reminder_text = row
        schedule_reminders(parser.parse(reminder_time), reminder_text)
        print(f"Reminder: '{reminder_text}' will ring 2 times starting from {reminder_time}")

    while True:
        schedule.run_pending()
        time.sleep(1)
        first_reminders_triggered = len([job for job in schedule.get_jobs() if 'reminder' in job.tags and 'first' in job.tags and job.last_run is not None])
        second_reminders_triggered = len([job for job in schedule.get_jobs() if 'reminder' in job.tags and 'second' in job.tags and job.last_run is not None])

        if first_reminders_triggered == len(rows) and second_reminders_triggered == len(rows):
            print(f"All reminders have run 2 times. Exiting.")
            break

    conn.close()

if __name__ == "__main__":
    main()

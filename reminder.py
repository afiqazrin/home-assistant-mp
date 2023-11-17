import schedule
from dateutil import parser
from texttospeech import speak
def check_reminder(columns):
    for column in columns:
        reminder_time = column[0]
        reminder_text = column[1]
        # print(reminder_time)
        # print(reminder_text)
        parsed_reminder_time = parser.parse(reminder_time)
        schedule_reminders(parsed_reminder_time, reminder_text)

    while True:
        schedule.run_pending()
        
def schedule_reminders(reminder_time, reminder_text):
    schedule.every().day.at(reminder_time.strftime('%H:%M')).do(reminder_callback, reminder_text, reminder_time, reminder_text).tag('reminder').tag('first')
    # schedule.every().day.at(reminder_time.strftime('%H:%M')).do(reminder_callback, reminder_text, reminder_time, reminder_text).tag('reminder').tag('second')

def reminder_callback(message, reminder_time, reminder_text):
    speak(message)
    

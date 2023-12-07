from dateutil import parser
from texttospeech import speak
from datetime import datetime
import time

def check_reminder(columns):
    for column in columns:
        reminder_time = column[0]
        reminder_text = column[1]
        # print("Reminder Time:", reminder_time)
        # print("Reminder Text:", reminder_text)

    while True:
        current_datetime = datetime.now()
        formatted_nowtime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if the current time matches any reminder time
        for column in columns:
            reminder_time = column[0]
            reminder_text = column[1]
            # print("Reminder_time: ", reminder_time, "Now time: ", formatted_nowtime)
            if formatted_nowtime == reminder_time:
                reminder_callback(reminder_text)
                time.sleep(1)

def reminder_callback(reminder_text):
    speak(reminder_text)
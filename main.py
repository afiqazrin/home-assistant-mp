from speechtotext import *
from whatsapp import  send_message
from texttospeech import speak
from db import insert_contact_db, read_contact_db, insert_reminder_db, read_reminder_db
from reminder import check_reminder
from gesture import main_opencv
import threading
from dateutil import parser
def main():
  while True: 
        gesture_process = Process(target=main_opencv)
        gesture_process.start()
        columns = read_reminder_db()
        reminders_thread = threading.Thread(target=check_reminder, args=(columns,))
        gesture_thread.start()
        reminders_thread.start()
        text = speech_to_text()
        if text == 0:
            continue
        if "save a contact" in text:
            speak("Name of contact to save")
            name = speech_to_text()
            speak("Number of contact")
            number = "+65" + speech_to_text()
            speak("Saving name" + name + " with number" + number + " in contacts")
            insert_contact_db(name, number)
        elif "send a message" in text: 
            speak("Who should I send a message to?")
            contact_name = speech_to_text().lower()
            while read_contact_db(contact_name) == None:
                speak("Name not found in contacts, please enter again")
                contact_name = speech_to_text().lower()
            number = read_contact_db(contact_name)
            speak("What message do you want to send?")
            message = speech_to_text()
            send_message(number, message)
        elif "set a reminder" in text:
            speak(f"What reminder do you want to set?")
            reminder_text = speech_to_text()
            speak(f"What deadline do you want to set for this reminder?")
            reminder_time = speech_to_text()
            parsed_reminder_time = parser.parse(reminder_time)
            print(parsed_reminder_time)
            insert_reminder_db(parsed_reminder_time, reminder_text)
        elif "bye" in text:
            speak("bye")
if __name__ == "__main__":
    main()
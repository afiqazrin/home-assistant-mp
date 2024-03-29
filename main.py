from speechtotext import speech_to_text
from whatsapp import send_message
from texttospeech import speak
from characterai import send_query
from projectdb import (
    insert_contact_db,
    read_contact_db,
    insert_reminder_db,
    read_reminder_db,
    is_emergency_saved,
    find_emergency_contact,
    read_bulbs_db
)
from reminder import check_reminder
from opencvfunctions import process_frame
import threading
from multiprocessing import Process
from dateutil import parser
import time
# import websockets
import queue
from bulb import initLightBulb, turnOffLightBulb, turnOnLightBulb, setBulbColor
import re
help_keywords = [
    "help",
    "assist",
    "support",
    "guide",
    "emergency",
    "need help",
    "help me",
    "can you help",
    "assist me",
    "urgent help",
]
question_keywords = ["who", "what", "where", "why", "when", "how"]
isBulbOn = False
def save_emergency_contact():
    speak("Please save an emergency contact")
    confirmed = False
    while not confirmed:
        speak("Name of emergency contact to save")
        name = speech_to_text().lower()

        speak("Number of emergency contact to save")
        number_input = speech_to_text()

        # Extract only digits from the input phone number
        number = "+"+extract_phone_number(number_input)
        speak(f"You want to save a contact named {name} and number of ")
        for digit in number:
            speak(digit)
        speak("Is that correct? Please say yes or no.")
        confirmation = speech_to_text().lower()
        if "yes" in confirmation:
            confirmed = True
            speak("Saving contact")
            insert_contact_db(name, number, 1)

        elif "no" in confirmation:
            confirmed = False
        else:
            speak("Sorry, I didn't catch that. Please say yes or no.")


def extract_phone_number(input_string):
    # Use a regular expression to match only digits
    digit_regex = re.compile(r"\D")
    # Remove non-digit characters
    phone_number = re.sub(digit_regex, "", input_string)
    return phone_number
def main():
    global isBulbOn
    # Check if the emergency contact has already been saved
    if not is_emergency_saved():
        save_emergency_contact()
    else:
        find_emergency_contact()

    person_detection_process = Process(target=process_frame, args=("person_detection",))
    person_detection_process.start()
    speak("Starting movement detection")
    
    while True:
        # constantly reading reminder db in a seperate thread to check the validity of reminders
        columns = read_reminder_db()
        reminders_thread = threading.Thread(target=check_reminder, args=(columns,))
        reminders_thread.start()
        text = speech_to_text()
        if text == 0:
            continue
        # saving of contacts to use in sending message function
        if "save a contact" in text:
            confirmed = False
            while not confirmed:
                speak("Name of contact to save")
                name = speech_to_text().lower()
                speak("Number of contact to save")
                number_input = speech_to_text()
                # Extract only digits from the input phone number
                number = "+"+extract_phone_number(number_input)
                speak(f"You want to save a contact named {name} and number of ")
                for digit in number:
                    speak(digit)
                speak("Is that correct? Please say yes or no.")
                confirmation = speech_to_text().lower()
                if "yes" in confirmation:
                    confirmed = True
                    speak("Saving contact")
                    insert_contact_db(name, number, 0)

                elif "no" in confirmation:
                    confirmed = False
                else:
                    speak("Sorry, I didn't catch that. Please say yes or no.")


        # sending of message function
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
        # setting a reminder function
        elif "set a reminder" in text:
            speak("What reminder do you want to set?")
            reminder_text = speech_to_text()
            while True:
                speak("What is the time you want to set for this reminder?")
                reminder_time = speech_to_text()
                try:
                    parsed_reminder_time = parser.parse(reminder_time)
                    insert_reminder_db(parsed_reminder_time, reminder_text)
                    speak("Reminder has been set")
                    break  # Exit the loop if the reminder is successfully set
                except ValueError:
                    speak("Incorrect time format, please try again")
        # controling of system controls such as volume and screen brightness
        elif "adjust system controls" in text:
            speak("Adjust systems control function started")
            person_detection_process.terminate()
            time.sleep(1)
            systems_control_process = Process(
                target=process_frame, args=("system_control",)
            )
            systems_control_process.start()
            time.sleep(15)
            systems_control_process.terminate()
            time.sleep(1)
            person_detection_process = Process(
                target=process_frame, args=("person_detection",)
            )
            person_detection_process.start()
            speak("Person detection started")

        # controlling of Tuya Light Bulb
        elif "control light bulb" in text:
            speak("What lightbulb do you want to control?")
            bulb_choice = speech_to_text()
            while read_bulbs_db(bulb_choice) == None:
                speak("Bulb not found in database, please try again")
                bulb_choice = speech_to_text().lower()
            device_id, local_key = read_bulbs_db(bulb_choice)
            initLightBulb(device_id, local_key)
            speak("Light bulb control function started")
            while True:
                control_choice = speech_to_text()
                if "switch on" in control_choice:
                    speak("Turning on lightbulb")
                    turnOnLightBulb()
                    isBulbOn = True
                elif "switch off" in control_choice:
                    speak("Turning off lightbulb")
                    turnOffLightBulb()
                    isBulbOn = False
                elif "change color" in control_choice:
                    if isBulbOn == False:
                        turnOnLightBulb()
                    speak("What color do you want to set?")
                    color = speech_to_text()
                    setBulbColor(color)
                elif "change brightness" in control_choice:
                    if isBulbOn == False:
                        turnOnLightBulb()
                    person_detection_process.terminate()
                    time.sleep(1)
                    bulb_control_process = Process(
                        target=process_frame, args=("bulb_control",)
                    )
                    bulb_control_process.start()
                    time.sleep(15)
                    bulb_control_process.terminate()
                    time.sleep(1)
                    person_detection_process = Process(
                        target=process_frame, args=("person_detection",)
                    )
                    person_detection_process.start()
                    speak("Person detection started")

                elif "stop" in control_choice:
                    speak("Exiting light bulb control function")
                    break
        # emergency sos function
        elif any(keyword in text for keyword in help_keywords):
            send_message(find_emergency_contact(), "Person requires immediate assistance")
        elif any("hello" in text and keyword in text for keyword in question_keywords):
            try:
                send_query(text + " in one sentence")
            except:
                speak("Couldn't connect to Character AI server. Please try again later.")

if __name__ == "__main__":
    main()

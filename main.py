# def mainFunction(text):
#     if(text == "save contact"):
#         print('yes')
#     elif(text == "send a message"):
#         print('no')
from speechtotext import *
from whatsapp import  send_message
from texttospeech import speak
from db import insert_contact_db, read_contact_db
def main():
  while True: 
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
        elif "bye" in text:
            speak("bye")
if __name__ == "__main__":
    main()
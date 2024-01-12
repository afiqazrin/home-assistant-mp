import speech_recognition as sr
import pywhatkit
r = sr.Recognizer()
def speech_to_text():

    while True:  # Continue looping until a valid text is obtained
        with sr.Microphone() as source:
            print("Adjusting for ambience noise, please wait...")
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source, phrase_time_limit=5)
            try:
                text = r.recognize_google(audio)
                print(text)
                return text  # Return the valid text and exit the loop
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that. Please try again.")


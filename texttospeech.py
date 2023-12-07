import pyttsx3

def speak(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    volume = engine.getProperty(
        "volume"
    )  # getting to know current volume level (min=0 and max=1)
    engine.setProperty("volume", 1.0)  # setting up volume level  between 0 and 1
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    rate = engine.getProperty("rate")  # getting details of current speaking rate
    engine.setProperty("rate", 100)  # setting up new voice rate
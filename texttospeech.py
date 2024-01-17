import pyttsx3

def speak(command):
    # Initialize the engine
    engine = pyttsx3.init()
    volume = engine.getProperty(
        "volume"
    )  # getting to know current volume level (min=0 and max=1)
    engine.setProperty("volume", 1.0)  # setting up volume level  between 0 and 1
    engine.setProperty("voice", "english")
    rate = engine.getProperty("rate")  # getting details of current speaking rate
    engine.setProperty("rate", 150)  # setting up new voice rate
    engine.say(command)
    engine.runAndWait()
    
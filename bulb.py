import tinytuya
import webcolors
from texttospeech import speak
from speechtotext import speech_to_text
import time
from projectdb import read_bulbs_db
#using MERRICK WIFI!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
d = None
def initLightBulb(device_id, local_key):
    global d
    print("d", device_id)
    print("l", local_key)
    try:
        d = tinytuya.BulbDevice(
            dev_id = device_id,
            address="Auto",  # Or set to 'Auto' to auto-discover IP address
            local_key = local_key,
            version=3.3,
        )
        print(d.status())
    except Exception as e:
        print(f"An unexpected error occurred during initialization: {e}")
        # Handle other types of exceptions that may occur during initialization

def turnOnLightBulb():
    d.turn_on()

def turnOffLightBulb():
    d.turn_off()


def setBulbBrightness(value):
    print("setting brightness: ", value)
    d.set_brightness_percentage(value, nowait=False)


def color_name_to_rgb(color_name):
    try:
        rgb_tuple = webcolors.name_to_rgb(color_name)
        print(rgb_tuple.red)
        print(rgb_tuple.green)
        print(rgb_tuple.blue)
        return rgb_tuple
    except ValueError:
        print(f"Error: Color name '{color_name}' not recognized.")
        return None

def setBulbColor(color_name):
    try:
        rgb_tuple = webcolors.name_to_rgb(color_name)
        speak("Changing lightbulb colour")
        d.set_colour(rgb_tuple.red, rgb_tuple.green, rgb_tuple.blue)

    except ValueError:
        print(f"Error: Color name '{color_name}' not recognized.")
        speak("Sorry, I didn't recognize that color. Please try again.")
        color_name = speech_to_text()

import tinytuya
import webcolors
from texttospeech import speak
from speechtotext import speech_to_text
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


# Connect to Device
d = tinytuya.BulbDevice(
    dev_id='3866058070039f21ba4f',
    address='Auto',      # Or set to 'Auto' to auto-discover IP address
    local_key="?'`n+0Yb|t+7Yk%1", 
    version=3.3)
print(d.status())
def turnOnLightBulb():
    d.turn_on()
def turnOffLightBulb():
    d.turn_off()
def setBulbBrightness(value):
    d.set_brightness_percentage(value)
def setBulbColor(color_name):
    try:
        rgb_tuple = webcolors.name_to_rgb(color_name)
        print(rgb_tuple.red)
        print(rgb_tuple.green)
        print(rgb_tuple.blue)
        d.set_colour(rgb_tuple.red,rgb_tuple.green, rgb_tuple.blue)
    except ValueError:
        print(f"Error: Color name '{color_name}' not recognized.")
        speak("Sorry, I didn't recognize that color. Please try again.")
        color_name = speech_to_text()

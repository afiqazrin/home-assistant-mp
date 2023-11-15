# Import Librar# Import Libraries
import pywhatkit
import pyautogui
import time
from pynput.keyboard import Key, Controller


from tkinter import *
win = Tk() # Some Tkinter stuff
screen_width = win.winfo_screenwidth() # Gets the resolution (width) of your monitor
screen_height= win.winfo_screenheight() # Gets the resolution (height) of your monitor

def send_message(number, message):
    pywhatkit.sendwhatmsg_instantly(number, message, 10)
    pyautogui.moveTo(screen_width * 0.694, screen_height* 0.964) # Moves the cursor the the message bar in Whatsapp
    pyautogui.click() # Clicks the bar
    pyautogui.press('enter') # Sends the message
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    keyboard.press('W')
    time.sleep(5)
    keyboard.press(Key.enter)
    keyboard.release(Key.ctrl)
    keyboard.release('W')
    keyboard.release(Key.enter)
    with open('PyWhatKit_DB.txt', 'w') as f:
        f.write("")
        f.close



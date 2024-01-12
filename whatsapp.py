import pywhatkit
import pyautogui
import time
import os


from tkinter import *
win = Tk()
screen_width = win.winfo_screenwidth() # Gets the resolution (width) of your monitor
screen_height= win.winfo_screenheight() # Gets the resolution (height) of your monitor

def send_message(number, message):
    pywhatkit.sendwhatmsg_instantly(number, message, 15)
    time.sleep(25)
    # pywhatkit.sendwhatmsg_instantly(number, message, 10, 15)
    #                                 )
    pyautogui.moveTo(screen_width * 0.694, screen_height* 0.964)
    pyautogui.click()
    pyautogui.press('enter')      
    time.sleep(5)
    pyautogui.hotkey("ctrl", "w")
    # pywhatkit creates/updates a txt file of all messages that has been sent through it everytime the function is run, this is unnecessary therefore we remove it                 
    with open('PyWhatKit_DB.txt', 'w') as f:
        os.remove('PyWhatKit_DB.txt')


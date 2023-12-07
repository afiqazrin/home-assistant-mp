import pywhatkit
import pyautogui
import time
import os
from pynput.keyboard import Key, Controller


from tkinter import *
win = Tk()
screen_width = win.winfo_screenwidth() # Gets the resolution (width) of your monitor
screen_height= win.winfo_screenheight() # Gets the resolution (height) of your monitor

def send_message(number, message):
    pywhatkit.sendwhatmsg_instantly(number, message, 10)
    pyautogui.moveTo(screen_width * 0.694, screen_height* 0.964) #                      ^
    pyautogui.click()                                            #                      |
    pyautogui.press('enter')                                     #                      |
    keyboard = Controller()                                      #                      |
    keyboard.press(Key.ctrl)                                     #                      |
    keyboard.press('W')                                          #                      |
    keyboard.release(Key.ctrl)                                   #                      |
    keyboard.release('W')                                        #       these lines of code are responsible for closing the whatsapp web tab after sending a message 
    time.sleep(5)                                                #                      |
    keyboard.press(Key.enter)                                    #                      |                                                                 #                      |
    keyboard.release(Key.enter)                                  #                      v
    # pywhatkit creates/updates a txt file of all messages that has been sent through it everytime the function is run, this is unnecessary therefore we remove it                 
    with open('PyWhatKit_DB.txt', 'w') as f:
        os.remove('PyWhatKit_DB.txt')

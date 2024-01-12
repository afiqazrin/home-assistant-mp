import sqlite3
import asyncio

async def allContact():
    connection_obj =sqlite3.connect(r"/home/pi/Desktop/home-assistant-mp/database/contacts.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("select * from contacts")
    contact = cursor_obj.fetchall()
    connection_obj.close()
    return contact
def deletecontact(name ,number):
    connection_obj =sqlite3.connect(r"/home/pi/Desktop/home-assistant-mp/database/contacts.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DELETE FROM contacts WHERE name = ? AND number = ?", (name, number))
    connection_obj.commit()
    connection_obj.close()
def adddbcontact(name ,number):
    connection_obj =sqlite3.connect(r"/home/pi/Desktop/home-assistant-mp/database/contacts.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("insert into contacts(name,number,isEmergency) values(?,?,0)", (name, number))
    connection_obj.commit()
    connection_obj.close()

def editcontact(name,number,oldname,oldnumber):
    connection_obj =sqlite3.connect(r"/home/pi/Desktop/home-assistant-mp/database/contacts.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("update contacts set number=?, name=? where number=? and name=?",(number,name,oldnumber,oldname))
    connection_obj.commit()
    connection_obj.close()


import sqlite3
import asyncio

async def allBulb():
    connection_obj =sqlite3.connect(r"/home/pi/Desktop/home-assistant-mp/database/bulbs.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("select * from bulbs")
    contact = cursor_obj.fetchall()
    connection_obj.close()
    return contact
def deleteBulb(id):
    connection_obj =sqlite3.connect(r"/home/pi/Desktop/home-assistant-mp/database/bulbs.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DELETE FROM bulbs WHERE device_id = ?", (id,))
    connection_obj.commit()
    connection_obj.close()
def addBulb(name ,id, key):
    connection_obj =sqlite3.connect(r"/home/pi/Desktop/home-assistant-mp/database/bulbs.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("insert into bulbs(name, device_id, local_key) values (?, ?, ?)", (name, id, key))
    connection_obj.commit()
    connection_obj.close()

def editBulb(name,device_id,local_key,oldid):
    connection_obj =sqlite3.connect(r"/home/pi/Desktop/home-assistant-mp/database/bulbs.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("update bulbs set device_id=?, name=?,local_key=? where device_id=?",(device_id,name,local_key,oldid))
    connection_obj.commit()
    connection_obj.close()

def getrow(name):
    connection_obj =sqlite3.connect(r"/home/pi/Desktop/home-assistant-mp/database/bulbs.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    RowData=cursor_obj.execute("select * from bulbs where name=?", (name,))
    for columns in RowData:
        name=columns[0]
        RowId=columns[1]
        key=columns[2]

    connection_obj.close()
    return name,RowId,key
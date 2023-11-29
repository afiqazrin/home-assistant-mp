import sqlite3
import asyncio


async def top3rang():
    connection_obj =sqlite3.connect(r"/home/afiq/home-assistant-mp/database/reminders.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("select *, datetime(reminder_time) as p from reminders where p<datetime('now','localtime')  ORDER by p DESC limit 3")
    top_3 = cursor_obj.fetchall()
    connection_obj.close()
    return top_3
async def top3coming():
    connection_obj =sqlite3.connect(r"/home/afiq/home-assistant-mp/database/reminders.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("select *, datetime(reminder_time) as p from reminders where p>datetime('now','localtime')  ORDER by p ASC limit 3")
    future_3 = cursor_obj.fetchall()
    connection_obj.close()
    return future_3
async def allreminder():
    connection_obj =sqlite3.connect(r"/home/afiq/home-assistant-mp/database/reminders.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("select * from reminders where julianday(datetime('now','localtime'))-julianday(reminder_time)<2")
    reminder = cursor_obj.fetchall()
    connection_obj.close()
    return reminder
def deletealarm(description ,time):
    connection_obj =sqlite3.connect(r"/home/afiq/home-assistant-mp/database/reminders.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DELETE FROM reminders WHERE reminder_text = ? AND reminder_time = ?", (description, time))
    connection_obj.commit()
    connection_obj.close()
def insertalarm(desc,time):
    connection_obj =sqlite3.connect(r"/home/afiq/home-assistant-mp/database/reminders.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("insert into reminders(reminder_time,reminder_text) values(?,?)", (time, desc))
    connection_obj.commit()
    connection_obj.close()
def editalarm(updated_description, updated_time, original_description, original_time):
    connection_obj =sqlite3.connect(r"/home/afiq/home-assistant-mp/database/reminders.db", check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("UPDATE reminders SET reminder_text=?, reminder_time=? WHERE reminder_text=? AND reminder_time=?",
                       (updated_description, updated_time, original_description, original_time))
    connection_obj.commit()
    connection_obj.close()

from flask import Flask, render_template,request,redirect,url_for,jsonify
from weather import dashboardsent
import asyncio
import threading
import schedule
import time
import webbrowser
from ReminderSQL import top3rang, top3coming, allreminder, deletereminder, insertreminder, editreminder
from ContactSQL import allContact,deletecontact,adddbcontact,editcontact
app = Flask(__name__, static_folder=r"/home/afiq/mp-2/home-assistant-mp/frontend")
from datetime import datetime



tempc = None
desc = None
humid=None
async def update_dashboard():
    global tempc, desc, humid
    tempc, desc, humid = await dashboardsent()
    
async def update_reminder():
    global top_3,future_3
    top_3=await top3rang()
    future_3=await top3coming()
async def getreminder():
    global reminder
    reminder=await allreminder()
async def getcontact():
    global contact
    contact=await allContact()

def job():
    asyncio.run(update_dashboard())
def job2():
    asyncio.run(update_reminder())
def job3():
    asyncio.run(getreminder())
def job4():
    asyncio.run(getcontact())
# Schedule the job function to run every minute
schedule.every(1).minutes.do(job)
schedule.every(0.01).minutes.do(job2)
schedule.every(0.01).minutes.do(job3)
schedule.every(0.01).minutes.do(job4)

def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(0.1)

# Start the scheduler thread
threading.Thread(target=scheduler_thread, daemon=True).start()

@app.route('/')
def home():
    return render_template('main.html')
    
@app.route('/dashboard')
def dashboard():
    job2()

    try:
            job()
            if desc.lower()=='SUNNY'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0001_sunny.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='PARTLY CLOUDY'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0002_sunny_intervals.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='CLOUDY'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0003_white_cloud.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='VERY CLOUDY'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0004_black_low_cloud.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='FOG'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0006_mist.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='LIGHT SHOWERS'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0009_light_rain_showers.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='LIGHT SLEET SHOWERS'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0013_sleet_showers.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='LIGHT SLEET'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0021_cloudy_with_sleet.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='THUNDERY SHOWERS'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0016_thundery_rain_showers.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='LIGHT SNOW'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0019_cloudy_with_light_snow.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='HEAVY SNOW'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0020_cloudy_with_heavy_snow.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='LIGHT RAIN'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0017_cloudy_with_light_rain.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='HEAVY SHOWERS'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0010_heavy_rain_showers.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='HEAVY RAIN'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0018_cloudy_with_heavy_rain.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='LIGHT SNOW SHOWERS'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0011_light_snow_showers.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='HEAVY SNOW SHOWERS'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0012_heavy_snow_showers.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='THUNDERY HEAVY RAIN'.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0024_thunderstorms_with_rain.png',top_3=top_3,future_3=future_3)
            elif desc.lower()=='THUNDERY SNOW SHOWERS '.lower():
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='frontend/templates/png/wsymbol_0016_thundery_snow_showers.png',top_3=top_3,future_3=future_3)
            else:
                return render_template('dashboard.html', tempc=tempc, desc=desc, humid=humid, wimage='abc', top_3=top_3,future_3=future_3)
    except Exception as e:
            print(e)
            return render_template('dashboard.html', tempc="", desc="Sorry, Could't connect to server please check your internet or try again later.", humid="", wimage="frontend/templates/png/nowifi.png", top_3=top_3,future_3=future_3)

        
        
# frontend/templates/png/temp2.png
@app.route('/reminder')
def reminder():
    job3()
    reminder = asyncio.run(allreminder())  # Retrieve reminders directly
    return render_template('reminder.html', reminder=reminder)

@app.route('/contact')
def contact():
    job4
    contact=asyncio.run(allContact())
    return render_template('contact.html', contact=contact)

@app.route('/deletereminder', methods=['POST'])
def delete_reminder_item():
    description = request.form.get('description')
    time = request.form.get('time')
    deletereminder(description, time)
    return '', 204 
@app.route('/deletecontact', methods=['POST'])
def delete_contact_item():
    name = request.form.get('uname')
    number = request.form.get('unumber')
    deletecontact(name ,number)
    return '', 204 
@app.route('/submitreminder', methods=['POST'])
def submit():
    data = request.json  # Get the JSON data sent from the popup
    desc = data.get('description')
    time = data.get('reminderTime')
    dt_object = datetime.strptime(time, '%Y-%m-%dT%H:%M')
    formatted_datetime = dt_object.strftime('%Y-%m-%d %H:%M:%S')


    insertreminder(desc,formatted_datetime)
    # ...

    return '',204  # Send a response (optional)
@app.route('/addreminder')
def addreminder():
    return render_template('addreminder.html')

@app.route('/addcontact')
def addcontact():
    return render_template('addcontact.html')

@app.route('/editreminder', methods=['GET', 'POST'])
def edit_reminder():
    if request.method == 'GET':
        description = request.args.get('description')
        time = request.args.get('time')
        return render_template('edit_reminder.html', description=description, time=time)
    elif request.method == 'POST':
        original_description = request.form.get('original_description')
        original_time = request.form.get('original_time')
        updated_description = request.form.get('description')
        updated_time = request.form.get('time')
        dt_object = datetime.strptime(updated_time, '%Y-%m-%dT%H:%M')
        formatted_datetime = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        editreminder(updated_description, formatted_datetime, original_description, original_time)
        return '',204
@app.route('/addedcontact', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']  # Getting the name field value
        country_code = request.form['countryCode']  # Getting the country code value
        phone_number = request.form['phoneNumber']  # Getting the phone number value
        fullnumber=country_code+phone_number
        adddbcontact(name,fullnumber)
        
        # Do something with the data (e.g., print it)
        print(f"Name: {name}, Country Code: {country_code}, Phone Number: {phone_number}")


        return '', 204
@app.route('/editcontact', methods=['GET', 'POST'])
def edithtmlcontact():
    if request.method == 'GET':
        name = request.args.get('name')
        number = request.args.get('number')
        print(number)
        return render_template('edit_contact.html', name=name, number=number)
    elif request.method == 'POST':
        original_name = request.form.get('contact_name')
        original_phoneno = request.form.get('contact_phone_number')
        updated_name = request.form.get('name')
        updated_no = request.form.get('phoneNumber')
        editcontact(updated_name,updated_no,original_name,original_phoneno)
        return '', 204



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/', new=2, autoraise=True)
    app.run(threaded=True)
    
 

    
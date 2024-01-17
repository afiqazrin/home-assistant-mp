import requests
from texttospeech import speak
api_url = 'http://192.168.130.58:5000/send_message'

def send_query(query):
    try:
        payload = {'message': query}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            data = response.json()
            # name = data.get('name')
            text = data.get('text')
            speak(text)
        elif response.status_code == 400:
            print(f"Error: {response.json()['error']}")
        else:
            print(f"Unexpected error: {response.text}")

    except Exception as e:
        print(f"Error: {str(e)}")
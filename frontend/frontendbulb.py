import tinytuya
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

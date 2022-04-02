
def transform_strings(logs):
    event = {'ACCESSIBILITY': 1,
             'ACCESSIBILITY_BROWSER_URL': 2,
             'ACCESSIBILITY_KEYBOARD_INPUT': 3,
             'APPS_INSTALL': 4,
             'AIRPLANEMODE': 5,
             'ACCELEROMETER': 6,
             'ACTIVITY': 7,
             'BLUETOOTH': 8,
             'BOOT': 9,
             'DATA_TRAFFIC': 10,
             'DEVICE_INFO': 11,
             'ESM': 12,
             'GYROSCOPE': 13,
             'INTERNET': 14,
             'INSTALLED_APP': 15,
             'LIGHT': 16,
             'NOTIFICATION': 17,
             'PHONE_ORIENTATION': 18,
             'PHONE': 19,
             'POWER': 20,
             'PROXIMITY': 21,
             'RINGER_MODE': 22,
             'SCREEN': 23,
             'SCREEN_ORIENTATION': 24,
             'SMS': 25,
             'USAGE_EVENTS': 26
             }


    logs['eventName'].replace(event, inplace=True)
    logs[logs['event'] == 1].replace(event, inplace=True)

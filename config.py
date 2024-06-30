import ubinascii              # To convert unique id to hex
import machine                # To get unique id

# Wireless network
WIFI_SSID = 'YOUR_WIFI_SSID'
WIFI_PASS = 'YOUR_WIFI_PASS'

# Adafruit IO (AIO) configuration
AIO_SERVER = 'io.adafruit.com'
AIO_PORT = 1883
AIO_USER = 'YOUR_ADAFRUIT_ID'
AIO_KEY = 'YOUR_ADAFRUIT_KEY'
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_HUMIDITY_FEED = 'PATH_TO_HUMIDITY_FEED'
AIO_TEMPERATURE_FEED=  'PATH_TO_TEMPERATURE_FEED'
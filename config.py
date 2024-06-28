import ubinascii              # Conversions between binary data and various encodings
import machine                # To Generate a unique id from processor

# Wireless network
WIFI_SSID = '*******'
WIFI_PASS = '*******'

# Adafruit IO (AIO) configuration
AIO_SERVER = 'i*******'
AIO_PORT = 1883
AIO_USER = '*******'
AIO_KEY = '*******'
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_LIGHTS_FEED = '*******'
AIO_RANDOMS_FEED = '*******'
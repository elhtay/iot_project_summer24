import ubinascii              # Conversions between binary data and various encodings
import machine                # To Generate a unique id from processor

# Wireless network
WIFI_SSID = 'Tele2_'
WIFI_PASS = 'ej'

# Adafruit IO (AIO) configuration
AIO_SERVER = 'io.adafru'
AIO_PORT = 1883
AIO_USER = ''
AIO_KEY = 'aio_VKnq09sRk8LzwRxNXFgt1G'
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_LIGHTS_FEED = 'elhtay/feeds/'
AIO_RANDOMS_FEED = 'elhtay/feeds/r'
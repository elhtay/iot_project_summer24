import time   
# Allows use of time.sleep() for delays
from mqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython code
import random                 # Random number generator
from machine import Pin       # Define pin
import config                   # Contain all keys used here
from  wifiConnection  import WifiConnection       # Contains functions to connect/disconnect from WiFi 
from dht import DHT11


# BEGIN SETTINGS
# These need to be change to suit your environment
RANDOMS_INTERVAL = 20000    # milliseconds
last_random_sent_ticks = 0  # milliseconds
led = Pin("LED", Pin.OUT)   # led pin initialization for Raspberry Pi Pico W


# Callback Function to respond to messages from Adafruit IO
def sub_cb(topic, msg):          # sub_cb means "callback subroutine"
    print((topic, msg))          # Outputs the message that was received. Debugging use.
    if msg == b"ON":             # If message says "ON" ...
        led.on()                 # ... then LED on
    elif msg == b"OFF":          # If message says "OFF" ...
        led.off()                # ... then LED off
    else:                        # If any other message is received ...
        print("Unknown message") # ... do nothing but output that it happened.
# Function to generate a random number between 0 and the upper_bound
def random_integer(upper_bound):
    return random.getrandbits(32) % upper_bound

# Function to publish random number to Adafruit IO MQTT server at fixed interval
def send_random():
    global last_random_sent_ticks
    global RANDOMS_INTERVAL

    if ((time.ticks_ms() - last_random_sent_ticks) < RANDOMS_INTERVAL):
        return; # Too soon since last one sent.

    some_number = random_integer(100)
    print("Publishing: {0} to {1} ... ".format(some_number, config.AIO_RANDOMS_FEED), end='')
    try:
        client.publish(topic=config.AIO_RANDOMS_FEED, msg=str(some_number))
        print("DONE")
    except Exception as e:
        print("FAILED")
    finally:
        last_random_sent_ticks = time.ticks_ms()


_wifiConnection =  WifiConnection()
# Try WiFi Connection
try:
    ip = _wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(config.AIO_CLIENT_ID, config.AIO_SERVER, config.AIO_PORT, config.AIO_USER, config.AIO_KEY)

# Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
client.subscribe(config.AIO_LIGHTS_FEED)
print("Connected to %s, subscribed to %s topic" % (config.AIO_SERVER, config.AIO_LIGHTS_FEED))

i = 0 
try:                      # Code between try: and finally: may cause an error
                          # so ensure the client disconnects the server if
                          # that happens.
    sensor = DHT11(Pin(13))
    while  i< 5:              # Repeat this loop forever
        client.check_msg()# Action a message if one is received. Non-blocking.
        send_random() 
        try:   
            sensor.measure()
            t = sensor.temperature()
            time.sleep(5)
            h = sensor.humidity()
            print('Sensor data successfully received, temperature:',t, 'humidity:', h )
            print('Next data in five seconds...')
            i+=1 
            
        except Exception as e:
            print("An exception occurred:", e)
            continue
            
            # Send a random number to Adafruit IO if it's time.
finally:                  # If an exception is thrown ...
    client.disconnect()   # ... disconnect the client and clean up.
    client = None
    _wifiConnection.disconnect()
    print("Disconnected from Adafruit IO.")
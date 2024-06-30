import time
from mqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
from machine import Pin       # Define pin
import config                   # Contain all keys used here
from  wifiConnection  import WifiConnection       # Contains functions to connect/disconnect from WiFi 
from dht import DHT11

# Initialize constant values
HUMIDITY_FEED= config.AIO_HUMIDITY_FEED
TEMPERATURE_FEED= config.AIO_TEMPERATURE_FEED

# Function to publish message to Adafruit IO MQTT server 
def sendMessage(message, aioFeed):

    # some_number = random_integer(100)
    print("Publishing: {0} to {1} and ... ".format(message, aioFeed), end='')
    try:
        client.publish(topic=aioFeed, msg=str(message))
        print("Done! Published: {0} to {1} and ... ".format(message, aioFeed), end='')
    except Exception as e:
        print("Failed to pushed")
    finally:
        last_random_sent_ticks = time.ticks_ms()

# **SET UP CONNECTIONS**
_wifiConnection =  WifiConnection()
# Try WiFi Connection
try:
    wifiConnectionResult = _wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt for WiFi Connection")

# Try MQTT Connection
try:
    print("Initializing MQTT Client")
    # Use the MQTT protocol to connect to Adafruit IO
    client = MQTTClient(config.AIO_CLIENT_ID, 
                        config.AIO_SERVER,
                        config.AIO_PORT, 
                        config.AIO_USER,
                        config.AIO_KEY)
    
    print("MQTT Client initialized successfully")
except OSError as e:
    print("MQTT Client initialization error:", e)
    raise  # Re-raise the exception for further investigation
except KeyboardInterrupt:
    print("Keyboard interrupt for MQTT Connection")

# Subscribed messages will be delivered to this callback
client.connect()

print("Connected to %s, subscribed to %s and %s topics" % (config.AIO_SERVER, HUMIDITY_FEED,  TEMPERATURE_FEED))

# Default value for number of data sent
i = 0 
try:                      # Code between try: and finally: may cause an error
                          # so ensure the client disconnects the server if
                          # that happens.
    sensor = DHT11(Pin(13))
    while  i < 5:              # Repeat this loop for 5 iterations (5 data points)
        client.check_msg()# Action a message if one is received. Non-blocking.
        try:   
            sensor.measure()
            
            # Fetch sensor data 
            temperatureData = sensor.temperature()
            humidityData = sensor.humidity()
            print('Sensor data successfully received, temperature:',temperatureData, 'humidity:', humidityData )
          
            time.sleep(5) # Delay for 5 seconds
            
            # Send Message humidity data to AIO
            sendMessage(humidityData, HUMIDITY_FEED) 
            print ("Humidity data sent to AIO")
            
            # Send Message temperature data to AIO
            sendMessage(temperatureData, TEMPERATURE_FEED)
            print ("Temperature data sent to AIO")
            
            print('Next data in five seconds...')
            print('-----------------------------------')
            print ('Number of data sent:', i+1)
            print ('Number of data are left:', 5-i-1)
            print('-----------------------------------')
            i+=1

        except Exception as e: # If an exception is thrown ...
            print("An exception occurred:", e)
            continue
# After the try: block is finished, run the code below to disconnect the client Wi-Fi and clean up.
finally:
    client.disconnect()
    client = None
    _wifiConnection.disconnect()
    _wifiConnection = None
    print("Disconnected from Adafruit IO.")
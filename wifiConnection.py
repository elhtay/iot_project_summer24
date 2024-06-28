import network
import config
from time import sleep

class WifiConnection:
    def __init__(self):
        self.ssid = config.WIFI_SSID
        self.password = config.WIFI_PASS
        self.wlan = network.WLAN(network.STA_IF)
        
    def connect(self):
        print('=>wifiId: '+ self.ssid )
        print('=>WifiPassword: ' + self.password )
        if not self.wlan.isconnected():  # Check if already connected
            print('Connecting to network...')
            self.wlan.active(True)  # Activate network interface
            # Set power mode to get WiFi power-saving off (if needed)
            self.wlan.config(pm=0xa11140)
            self.wlan.connect(self.ssid, self.password)  # Your WiFi credentials
            print('Waiting for connection...', end='')

            timeout = 60  # Set a longer timeout limit in seconds
            while not self.wlan.isconnected() and self.wlan.status() >= 0 and timeout > 0:
                print('.', end='')
                sleep(1)
                timeout -= 1

            if self.wlan.isconnected():
                ip = self.wlan.ifconfig()[0]
                print('\nConnected on {}'.format(ip))
                return ip
            else:
                print('\nFailed to connect to WiFi')
                self._print_status()
                return None
        else:
            ip = self.wlan.ifconfig()[0]
            print('Already connected on {}'.format(ip))
            return ip

    def http_get(self, url='http://detectportal.firefox.com/'):
        import socket  # Used by HTML get request
        import time  # Used for delay
        
        try:
            _, _, host, path = url.split('/', 3)  # Separate URL request
            print('==> host:', host)
            addr = socket.getaddrinfo(host, 80)[0][-1]  # Get IP address of host
            print('==> addr:', addr)
            
            s = socket.socket()  # Initialize the socket
            s.connect(addr)  # Try connecting to host address
            print('==> Connected to addr:', addr)
            
            # Send HTTP request to the host with specific path
            request = 'GET /{} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(path, host)
            s.send(request.encode('utf8'))  # Send the HTTP request
            time.sleep(1)  # Sleep for a second
            
            rec_bytes = s.recv(10000)  # Receive response
            print(rec_bytes.decode('utf8'))  # Print the response as a string
            s.close()  # Close connection
        except Exception as e:
            print("HTTP GET request failed:", e)

    def check_wifi_connection(self):
        if self.wlan.isconnected():
            print("WiFi is connected")
            return True
        else:
            print("WiFi is not connected")
            return False

    def _print_status(self):
        status = self.wlan.status()
        if status == network.STAT_IDLE:
            print("Status: IDLE")
        elif status == network.STAT_CONNECTING:
            print("Status: CONNECTING")
        elif status == network.STAT_WRONG_PASSWORD:
            print("Status: WRONG PASSWORD")
        elif status == network.STAT_NO_AP_FOUND:
            print("Status: NO AP FOUND")
        elif status == network.STAT_CONNECT_FAIL:
            print("Status: CONNECTION FAILED")
        else:
            print("Status: UNKNOWN ERROR", status)
    def disconnect(self):
        wlan = network.WLAN(network.STA_IF)  # Initialize WLAN interface
        if wlan.isconnected():
            wlan.disconnect()  # Disconnect from the current WiFi network
            print("Disconnected from WiFi")
        else:
            print("Already disconnected from WiFi")
        wlan.active(False)  # Deactivate the WLAN interface to save power
        wlan = None  # Clear the WLAN object 
        
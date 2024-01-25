# main.py -- put your code here!
# --------------------------------------------------
# Author: avsg8, (https://github.com/avsg8), 01/2024

from BaseMQ import BaseMQ 
from micropython import const
from network import WLAN, LTE, LoRa, Bluetooth
import machine, pycom, socket, uos, time #, ssl
from umqtt.simple2 import MQTTClient
from MQ7_main import App
from parse import urlencode
from urequest import urlopen

#---------------- deep sleep wake up block ------------------#
if pycom.lte_modem_en_on_boot():
    print("LTE on boot was enabled. Disabling.")
    pycom.lte_modem_en_on_boot(False)
(wake_reason, gpio_list) = machine.wake_reason()

## Print reason for wake up
print("Device running for: " + str(time.ticks_ms()) + "ms")
print("Remaining sleep time: " + str(machine.remaining_sleep_time()) + "ms" )
if wake_reason == machine.PWRON_WAKE:
    print("Woke up by reset button")
elif wake_reason == machine.PIN_WAKE:
    print("Woke up by external pin (external interrupt)")
    print(*gpio_list, sep=", ")
elif wake_reason == machine.RTC_WAKE:
    print("Woke up by RTC (timer ran out)")
elif wake_reason == machine.ULP_WAKE:
    print("Woke up by ULP (capacitive touch)")
#########
# machine.pin_sleep_wakeup(('P3', 'P4'), mode=machine.WAKEUP_ANY_HIGH, enable_pull=True)

#---------------- WiFi connection block ------------------#
wlan = WLAN(mode=WLAN.STA, antenna=WLAN.EXT_ANT, max_tx_pwr=78)

wlan.connect(ssid='<your-SSID-here>', auth=(WLAN.WPA2, '<your-wifi-pwd>'))
print('trying to connect to wifi')
for k in range(10):
    if wlan.isconnected():
        print("Wifi successfully connected @ try# ", k)
        break
    else:
        print("Not connected to wifi yet. Tries remaining:", (10-k))
        # machine.idle()      
        time.sleep(1)
while not wlan.isconnected():
   machine.idle()
print("WiFi connected succesfully")

print(wlan.ifconfig())

#---------------- gas sensing block ------------------#
val = App().Run()
print(val)
# some activity leds to let you know which step you are at
pycom.rgbled(0x7f7f00)

#--- umqtt testing block ----#
#s = socket.socket()
#ss = ssl.wrap_socket(s)
#ss.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
#print(ss)
# payload = int(uos.urandom(1)[0] / 256*10)
# temp = machine.temperature() #internal temperature of FiPy. May not be used at all
# payload = temp
#---- end testing block -----#

#---------------- MQTT block ------------------#
def pubmsg(server="localhost", topic='COlevels', payload=0):
    c = MQTTClient("umqtt_client", server)
    c.connect()
    c.publish(bytes(topic,'utf-8'), bytes(str(payload),'utf-8'))
    c.disconnect()
try:
    pubmsg(server='<ipaddress-of-your-nodered-mqtt-server>', topic='<your-mqtt-topic>', payload= val) # connects to a nodered broker on local network
                                                                                            # look in images folder for code
except:
    pass
print('rgbled lit')

#---------------- push notification block (simplepush.io) ------------------#
if val > 50: #or a set value
    data = urlencode({'key': '<your-simplepush-key-here>', 'title': 'CO level inside', 'msg': 'Check for high CO levels inside', 'event': 'warning'}).encode()
    urlopen("https://api.simplepush.io/send", data= data) #send msg to your phone

#---------------- get ready to go into deep sleep block ------------------#
print('Switching off LTE radio')
try:
    lte = LTE()
    lte.deinit()
except:
    pass
pycom.rgbled(0x00ff00)
time.sleep(1)
print('Switching off WLAN')
wlan.deinit()
pycom.rgbled(0x0000ff)
time.sleep(1)
print('Switching off Heartbeat')
pycom.rgbled(0xff0000)
time.sleep(1)

print('Switching off Bluetooth')
bt = Bluetooth()
bt.deinit()
pycom.rgbled(0xffffff)
time.sleep(1)

print('Switching off LoRa')
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915, power_mode=LoRa.SLEEP)
print("Going to sleep")

pycom.heartbeat(False)
pycom.rgbled(0x000000)

# Probably redundant to use machine deepsleep to conserve battery if the code is used to interface with MQ sensors. These sensors need
# a pre-heat time of few hours to couple of days to stabilize. So, it's does not make sense to power them from battery.
machine.deepsleep(1000*60)

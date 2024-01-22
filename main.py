# main.py -- put your code here!
# Author: avsg8. 01/20/2024

from network import WLAN, LTE, LoRa, Bluetooth, Server
import machine, pycom, socket, ssl, uos, time
from umqtt.simple2 import MQTTClient
from MQ7_main import App

#Deep sleep for power savings may be redundant if you are using with MQ sensors. Those sensors need a pre-heat time of few hours
# to couple of days for stable readings. So, no point powering them from battery. But will keep it here for other projects

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
    #print(*gpio_list, sep=", ")
elif wake_reason == machine.RTC_WAKE:
    print("Woke up by RTC (timer ran out)")
elif wake_reason == machine.ULP_WAKE:
    print("Woke up by ULP (capacitive touch)")
#########
machine.pin_sleep_wakeup(('P3', 'P4'), mode=machine.WAKEUP_ANY_HIGH, enable_pull=True)


def pubmsg(server="localhost", topic='saltlevel', payload=0):
    c = MQTTClient("umqtt_client", server)
    c.connect()
    c.publish(bytes(topic,'utf-8'), bytes(str(payload),'utf-8'))
    c.disconnect()

wlan = WLAN(mode=WLAN.STA, antenna=WLAN.EXT_ANT, max_tx_pwr=78)

wlan.connect(ssid='1234', auth=(WLAN.WPA2, 'xxxxxxxx'))
print('trying to connect to wifi')
for k in range(10):
    if wlan.isconnected():
        print("Wifi successfully connected @ try# ", k)
        break
    else:
        print("Not connected to wifi yet. Tries remaining:", (10-k))
        machine.idle()      
        time.sleep(1)
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())
s = socket.socket()
ss = ssl.wrap_socket(s)
ss.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
print(ss)

# payload = int(uos.urandom(1)[0] / 256*10) #testing umqtt with a random payload

val = App().Run() # Get CO value from sensor
temp = machine.temperature() # get internal temp of the FiPy, may not be used at all
pycom.rgbled(0x7f7f00) #some activity LED to let you know where things are at
try:
    pubmsg(server='192.168.86.124', topic='saltlevel', payload= val)
except:
    pass
#print('rgbled lit')

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

machine.deepsleep(1000*60)

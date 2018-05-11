import paho.mqtt.client as mqtt
import random
import time
import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 5
instance = dht11.DHT11(pin = 26)
### humid sensor

idx = 0

def getHumid(humid):
    msg = humid
    return msg

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_publish(client, userdata, mid):
    global idx
    idx = idx+1
    for i in range(idx):
        print "-",
    msg_id = mid
    if idx == 10 :
        idx = 0
    print("\n message published")

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# YOU NEED TO CHANGE THE IP ADDRESS OR HOST NAME
# pi
mqttc.connect("192.168.0.24")
# mac
# mqttc.connect("172.19.89.83")
#mqttc.connect("localhost")
mqttc.loop_start()

try:
    while True:
        if result.is_valid():
            result = instance.read()
            t = getMsg(result.humidity)
        else:
            t = "humid sensor error"

        (result, m_id) = mqttc.publish("environment/humidity", t)


		# print("Temperature: %d C" % result.temperature)
		# print("Humidity: %d %%" % result.humidity)

        time.sleep(2)

except KeyboardInterrupt:
    print("Finished!")
    mqttc.loop_stop()
    mqttc.disconnect()

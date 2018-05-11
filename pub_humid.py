import paho.mqtt.client as mqtt
import random
import time

### humid sensor

idx = 0

def getMsg():
    msg = str(random.randrange(30, 96))
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
        t = getMsg()
        (result, m_id) = mqttc.publish("home/humidity", t)
        time.sleep(2)

except KeyboardInterrupt:
    print("Finished!")
    mqttc.loop_stop()
    mqttc.disconnect()

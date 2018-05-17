import spidev
import time
import RPi.GPIO as gpio
import time
import paho.mqtt.client as mqtt


trig_pin = 19
echo_pin = 26

gpio.setmode(gpio.BCM)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 61000
idx = 0

def readChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((adc[1] & 3) << 8) + adc[2]
    return adc_out


def convert2volts(data, places):
    volts = (data * 3.3) / float(1023)
    volts = round(volts, places)
    return volts


def getMsg(distance):
    msg = distance
    return msg


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_publish(client, userdata, mid):
    global idx
    idx = idx+1
    for i in range(idx):
        print "-",
    msg_id = mid
    if idx == 10:
        idx = 0
    print("\n message published")


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# YOU NEED TO CHANGE THE IP ADDRESS OR HOST NAME
# pi
mqttc.connect("192.168.0.6")
mqttc.loop_start()

try:
    while True:
        # ultrasonic
        gpio.output(trig_pin, False)
        time.sleep(0.5)

        gpio.output(trig_pin, True)
        time.sleep(0.00001)
        gpio.output(trig_pin, False)

        while gpio.input(echo_pin) == 0:
            pulse_start = time.time()

        while gpio.input(echo_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 34000 / 2
        distance = round(distance, 2)

        # print("Distance : ", distance, "cm")
        # homework
        t = getMsg(distance)
        print(distance)
        (result, m_id) = mqttc.publish("environment/distance", t)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Finished")
    spi.close()
    gpio.cleanup()
    mqttc.loop_stop()
    mqttc.disconnect()




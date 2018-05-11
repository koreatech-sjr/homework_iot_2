import spidev
import time
import RPi.GPIO as gpio
import time
import paho.mqtt.client as mqtt

trig_pin = 13
echo_pin = 19

led_red_pin = 20
led_yellow_pin = 6
led_green_pin = 5
gpio.cleanup()
gpio.setmode(gpio.BCM)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)
gpio.setup(led_red_pin, gpio.OUT)
gpio.setup(led_yellow_pin, gpio.OUT)
gpio.setup(led_green_pin, gpio.OUT)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 61000

light_channel = 0
temp_channel = 1

temp = 0.0
humidity = 0.0

def readChannel(channel):
        adc = spi.xfer2([1, (8 + channel) << 4, 0])
        adc_out = ((adc[1] & 3) << 8) + adc[2]
        return adc_out

def convert2volts(data, places):
        volts = (data * 3.3) / float(1023)
        volts = round(volts, places)
        return volts

### subscribe
def on_connect_subscribe(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe("home/temperature")
    client.subscribe("home/humidity")

def on_message(client, userdata, msg):

    global temp
    global humidity

    print("Topic: " + msg.topic + " Message: " + str(msg.payload))

    if msg.topic == "home/temperature":
        temp = float(msg.payload)
    elif msg.topic == "home/humidity":
        humidity = float(msg.payload)

    print("temp :", temp)
    print("humidity :", humidity)

client = mqtt.Client()
client.on_connect = on_connect_subscribe
client.on_message = on_message
# pi
client.connect("192.168.0.24", 1883, 60)
client.loop_start()
try:
        while True:
                light_level = readChannel(light_channel)
                light_volts = convert2volts(light_level, 2)

                print("-------------------------------------")
                print("Light: %d (%f V)" %(light_level, light_volts))
                #ultrasonic
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

                print("Distance : ", distance, "cm")
                # homework
                if light_level <= 150:
                    gpio.output(led_green_pin, True)
                    gpio.output(led_yellow_pin, True)
                    gpio.output(led_red_pin, True)

                if distance >= 30 and light_level>151:
                    print('green')
                    gpio.output(led_green_pin,True)
                    gpio.output(led_yellow_pin, False)

                elif distance >= 10 and light_level>151:
                    print('yellow')
                    gpio.output(led_green_pin, False)
                    gpio.output(led_yellow_pin, True)
                    gpio.output(led_red_pin, False)

                elif distance <10 and light_level>151:
                    print('Red')
                    gpio.output(led_green_pin, False)
                    gpio.output(led_yellow_pin, False)
                    gpio.output(led_red_pin, True)

except KeyboardInterrupt:
        print("Finished")
        spi.close()
        gpio.cleanup()
        client.unsubscribe(["home/temperature", "home/humidity"])
        client.disconnect()

import spidev
import time
import RPi.GPIO as gpio
import time
import paho.mqtt.client as mqtt

led_red_pin = 5
led_yellow_pin = 6
led_green_pin = 13

gpio.setmode(gpio.BCM)
gpio.setup(led_red_pin, gpio.OUT)
gpio.setup(led_yellow_pin, gpio.OUT)
gpio.setup(led_green_pin, gpio.OUT)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 61000

temp_channel = 1

temp = 0.0
humidity = 0.0
distance = 0.0

flag = False
# subscribe


def on_connect_subscribe(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe("environment/temperature")
    client.subscribe("environment/humidity")
    client.subscribe("environment/distance")


def on_message(client, userdata, msg):

    global temp
    global humidity
    global distance
    global flag
    
    print("Topic: " + msg.topic + " Message: " + str(msg.payload))

    if msg.topic == "environment/temperature":
        if msg.payload==("temperature sensor error"):
            print("msg.payload")
        else :
            temp = msg.payload
            if float(temp) > 21 :
                flag = True;
                gpio.output(led_green_pin, True)
                gpio.output(led_yellow_pin, True)
                gpio.output(led_red_pin, True)
            else :
                flag = False
    
    elif msg.topic == "environment/humidity":
        if msg.payload==("humid sensor error"):
            print("msg.payload")
        else :
            humidity = msg.payload
            if float(humidity) > 25 :
                flag = True;
                gpio.output(led_green_pin, True)
                gpio.output(led_yellow_pin, True)
                gpio.output(led_red_pin, True)
            else :
                flag = False
    
    elif msg.topic == "environment/distance":
        distance = msg.payload
        distance = float(distance)
        if distance >= 30 and flag==False:
            gpio.output(led_green_pin, True)
            gpio.output(led_yellow_pin, False)
            gpio.output(led_red_pin, False)

        elif distance >= 10 and flag==False:
            gpio.output(led_green_pin, False)
            gpio.output(led_yellow_pin, True)
            gpio.output(led_red_pin, False)

        elif distance < 10 and flag==False:
            gpio.output(led_green_pin, False)
            gpio.output(led_yellow_pin, False)
            gpio.output(led_red_pin, True)



    print("temp :", temp)
    print("humidity :", humidity)
    print("disance :", distance)
    print("flag : ", flag)


client = mqtt.Client()
client.on_connect = on_connect_subscribe
client.on_message = on_message
# pi
client.connect("192.168.0.6", 1883, 60)

try:
    client.loop_forever()

except KeyboardInterrupt:
    print("Finished")
    spi.close()
    gpio.cleanup()
    client.unsubscribe(["environment/temperature", "environment/humidity", "environment/distance"])
    client.disconnect()

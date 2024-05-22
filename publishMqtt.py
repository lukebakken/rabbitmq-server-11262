import os
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
import time

connected = False
# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_publish(mosq, obj, mid):
    print("published: " + str(mid))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

url = urlparse('mqtt://localhost:1883')
# Connect
mqttc.username_pw_set('myuser', 'password')
mqttc.connect(url.hostname, url.port)


#while (connected != True):
#     time.sleep(1000)

for i in range(10):
    # Publish a message
    mqttc.publish("data/mqtt/type", "my message",0)
    time.sleep(1)


mqttc.disconnect()



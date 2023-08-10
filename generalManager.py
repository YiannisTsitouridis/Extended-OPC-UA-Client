import sys
import os
import time
import paho.mqtt.client as mqtt
from startUp import flag

def on_connect(agent, userdata, flags, rc):
    pass

def on_message(agent, userdata, msg):
    if msg.payload == "stop":
        flag = False
    elif msg.payload == "startUp"
        pass

def main():
    generalAgent = mqtt.Client("general")
    generalAgent.on_connect = on_connect
    generalAgent.on_message = on_message
    generalAgent.connect("localhost")
    generalAgent.subscribe("GeneralTopic")



import sys
import os
import time
import paho.mqtt.client as mqtt
from startUp import flag
import startUp

def on_connect(agent, userdata, flags, rc):
    agent.subscribe("generalManager")

def on_message(agent, userdata, msg):
    if msg.payload == "stop":
        flag = False
    elif msg.payload == "startUp":
        startUp

def main():
    generalAgent = mqtt.Client("general")
    generalAgent.on_connect = on_connect
    generalAgent.on_message = on_message
    generalAgent.connect("localhost")
    generalAgent.subscribe("GeneralTopic")



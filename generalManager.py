import sys
import os
import time
import paho.mqtt.client as mqtt
import startUp
from startUp import stop

def on_connect(agent, userdata, flags, rc):
    agent.subscribe("generalManager")

def on_message(agent, userdata, msg):
    if msg.payload == "stop":
        stop()
    elif msg.payload == "startUp":
        startUp

def main():
    generalAgent = mqtt.Client("general")
    generalAgent.on_connect = on_connect
    generalAgent.on_message = on_message
    generalAgent.connect("localhost")
    generalAgent.subscribe("GeneralTopic")



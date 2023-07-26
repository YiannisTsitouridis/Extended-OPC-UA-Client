import sys
import time
import paho.mqtt.client as mqtt

def on_connect():
    pass
def on_message():
    pass
def main():
    generalAgent = mqtt.Client()
    generalAgent.subscribe("GeneralTopic")



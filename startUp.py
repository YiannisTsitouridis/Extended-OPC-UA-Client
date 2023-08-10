#!/usr/bin/python3
import sys
import os
import asyncio
sys.path.insert(0, "..")
import asyncua
import logging
import time
from asyncua import common
from asyncua.common import node, subscription, shortcuts
from pathlib import Path
import numpy as np
import json
from asyncua import ua
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, tostring
from typing import List, Any
from dict2xml import dict2xml
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
import paho.mqtt.client as mqtt
from asyncua.sync import Client, ThreadLoop, _logger
import codecs
import sqlalchemy
import configparser
import threading
from opcUaClientClass import opcuaClient

# This part of code is for importing the appropriate console
try:
    from IPython import embed
    print("IPython module imported")
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()
        print("Code module imported")



############################################################################
####                     DEFINING MAIN FUNCTION                         ####
############################################################################

def startUp():
    serversData = configparser.ConfigParser()
    serversData.read("clientData.ini")
    numOfServers = serversData.getint('NumberOfServers', 'serversNum')
    clientsList = []
    kill = False
    for i in range(1, numOfServers + 1):
        localurl = serversData.get('Server' + str(i - 1), 'url')
        localname = serversData.get(('Server' + str(i - 1)), 'name')
        localmqttUrl = serversData.get(('Server' + str(i - 1)), 'mqttUrl')
        localmqttPort = serversData.get(('Server' + str(i - 1)), 'mqttPort')
        localarchitectureTopic = serversData.get(('Server' + str(i - 1)), 'architecturetopic')
        localconsoleTopic = serversData.get('Server' + str(i - 1), 'consoletopic')
        localreadTopic = serversData.get(('Server' + str(i - 1)), 'readtopic')
        print("Reached till here!" + '\n')
        with opcuaClient(localurl, localname, localmqttUrl, int(localmqttPort), localarchitectureTopic,
                         localconsoleTopic, localreadTopic) as client:
            try:
                client.connect()
                print("Server with name " + str(client.name) + " detected")
                time.sleep(2)
                clientsList.append(client)
            except:
                print("Error occurred while trying to connect to server" + str(client.name) + "with url:" + str(
                    client.url))
                client.agent.publish("Topic", "Error occurred while trying to connect to server" + str(
                    client.name) + " with url: " + str(client.url))
            resul = client.initial_subscriptions()
            tree = client.browse_server()
            treejs = json.dumps(tree)
            client.agent.publish("arch", treejs)
            embed()
            while not kill:
                time.sleep(0.1)
            else:
                client.disconnect()
                client.tloop.stop()



def main():
    global kill
    kill = False
    def on_connect(agent, userdata, flags, rc):
        print("Connected!")

    def on_message(agent, userdata, msg):
        print("Recieved something!")
        print(msg.payload)
        mess = str(msg.payload.decode("utf-8"))
        if mess == "stop":
            print("stop ordered")
            # startUp.stop()
            # runThread.start()
            kill = True
        elif mess == "startUp":
            print("startUp ordered")
            startUp()

    generalAgent = mqtt.Client("general")
    generalAgent.on_connect = on_connect
    generalAgent.on_message = on_message
    generalAgent.connect(host="localhost", port=1883)
    generalAgent.subscribe("generalTopic")
    generalAgent.loop_forever()

if __name__ == "__main__":
    main()

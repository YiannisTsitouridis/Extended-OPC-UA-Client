#!/usr/bin/python3
import sys
import os
import asyncio

import clientConfig

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
import paho.mqtt.client as mqtt
from asyncua.sync import Client, ThreadLoop, _logger
import codecs
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

clientsList = []

############################################################################
####                     DEFINING USEFUL FUNCTIONS                      ####
############################################################################

def startUp(numOfServers):
    kill = False
    # with ThreadPool() as pool:
    for i in range(1, numOfServers + 1):
        t = threading.Thread(target=startClient, args=(i,))
        clientsList.append(t)
        clientsList[i-1].start()

def startClient(num):
    serversData = configparser.ConfigParser()
    serversData.read("clientData.ini")
    localurl = serversData.get('Server' + str(num - 1), 'url')
    localname = serversData.get(('Server' + str(num - 1)), 'name')
    localmqttUrl = serversData.get(('Server' + str(num - 1)), 'mqttUrl')
    localmqttPort = serversData.get(('Server' + str(num - 1)), 'mqttPort')
    localarchitectureTopic = serversData.get(('Server' + str(num - 1)), 'architecturetopic')
    localconsoleTopic = serversData.get('Server' + str(num - 1), 'consoletopic')
    localreadTopic = serversData.get(('Server' + str(num - 1)), 'readtopic')
    with opcuaClient(localurl, localname, localmqttUrl, int(localmqttPort), localarchitectureTopic,
                     localconsoleTopic, localreadTopic) as client:
        try:
            client.__enter__()
            print("Server with name " + str(client.name) + " detected")
            clientsList.append(client)
        except:
            print("Error occurred while trying to connect to server" + str(client.name) + "with url:" + str(
                client.url))
            client.agent.publish("Topic", "Error occurred while trying to connect to server" + str(
                client.name) + " with url: " + str(client.url))
        tree = client.browse_server()
        treejs = json.dumps(tree)

        print(treejs)
        client.agent.publish("arch", treejs)
        embed()

def stop(numOfServers):
    print("All client instances are terminated.")
    for i in range(1, numOfServers):
        clientsList[i].stop()

############################################################################
####                     DEFINING MAIN FUNCTION                         ####
############################################################################
def main():
    serversData = configparser.ConfigParser()
    serversData.read("clientData.ini")
    numOfServers = serversData.getint('NumberOfServers', 'serversNum')

    def on_connect(agent, userdata, flags, rc):
        print("Connected!")

    def on_message(agent, userdata, msg):
        mess = str(msg.payload.decode("utf-8"))
        if msg.topic == "startStop":
            if mess == "stop":
                print("stop ordered")
                stop(numOfServers)
            elif mess == "startUp":
                print("startUp ordered")
                startUp(numOfServers)
        elif msg.topic == "initialize":
            clientConfig.initialize_from_UI(mess)
        elif msg.topic == "addServer":
            clientConfig.addserver_from_UI(mess)



    generalAgent = mqtt.Client("general")
    generalAgent.on_connect = on_connect
    generalAgent.on_message = on_message
    generalAgent.connect(host="test.mosquitto.org", port=1883)
    generalAgent.subscribe("startStop")
    generalAgent.loop_forever()






if __name__ == "__main__":
    main()

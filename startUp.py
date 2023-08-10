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

global flag

############################################################################
####                     DEFINING MAIN FUNCTION                         ####
############################################################################
def stop():
    flag = False
def main():
    serversData = configparser.ConfigParser()
    serversData.read("clientData.ini")
    numOfServers = serversData.getint('NumberOfServers', 'serversNum')
    clientsList = []
    flag =True
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





if __name__ == "__main__":
    main()

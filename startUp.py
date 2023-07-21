#!/usr/bin/python3
import sys
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

############################################################################
####                     DEFINING MAIN FUNCTION                         ####
############################################################################


def main():
    serversData = configparser.ConfigParser()
    serversData.read("clientData.ini")
    numOfServers = serversData.getint('NumberOfServers', 'serversNum')
    clientsList = []
    for i in range(1, numOfServers+1):
        with ThreadLoop() as tloop:
            localurl = serversData.get('Server' + str(i-1), 'url')
            localname = serversData.get(('Server' + str(i-1)), 'name')
            localmqttUrl = serversData.get(('Server' + str(i-1)), 'mqttUrl')
            localmqttPort = serversData.get(('Server' + str(i-1)), 'mqttPort')
            localarchitectureTopic = serversData.get(('Server' + str(i-1)), 'architecturetopic')
            localconsoleTopic = serversData.get('Server' + str(i-1), 'consoletopic')
            localreadTopic = serversData.get(('Server' + str(i-1)), 'readtopic')
            print("Reached till here!"+'\n')
            with opcuaClient(localurl, localname, localmqttUrl, int(localmqttPort), localarchitectureTopic, localconsoleTopic, localreadTopic) as client:
                try:
                    client.connect()
                    print("Server with name " + str(client.name) + " detected")
                    time.sleep(2)
                    clientsList.append(client)
                except:
                    print("Error occurred while trying to connect to server" + str(client.name) + "with url:" + str(client.url))
                    client.agent.publish("Topic", "Error occurred while trying to connect to server" + str(client.name) + " with url: " + str(client.url))
                tree = client.browse_server()
                treejs = json.dumps(tree)
                client.agent.publish("arch", treejs)
                print(client.name, " architecture posted:"+"\n \n", tree)
                ag = client.crea


            time.sleep(100)
    time.sleep(1000)


    # serversNumber = serverDataParser.getint('NumberOfServers', 'serversNum')
    # for i in range(0, serversNumber):
    #     url = serverDataParser.get("")
    #     object =
    # initial_configfile.add_section("Server" + str(numOfServers))
    # initial_configfile.set('Server', 'serversNum', serverUrl)
    # newNumOfServers = numOfServers + 1
    # initial_configfile.set('NumberOfServers', 'serversNum', newNumOfServers)





    # serverUrl = "opc.tcp://yiannis-Virtual-Machine:4841/"
    # client = opcuaClient(serverUrl)
    # try:
    #     client.connect()
    # except:
    #     print("Error occurred while trying to connect to server", str(serverUrl))
    #     #agent.publish("ex/client", "Error occurred while trying to connect to server"+str(serverUrl))




    # # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
    #
    # serverNodesString = str(serverNodes)
    #
    # print('Node tree:', [serverNodes])
    # print('\n', '\n', '\n')
    #
    # print(json.dumps(serverNodes))
    # print('\n','\n','\n')
    #
    # # Saving the information from the address space to the ServerNodes.xml file
    # xml = dict2xml(serverNodes)
    # print(xml)
    # f = open("ServerNodes.xml","w")
    # f.write(xml)
    # f.close()


    # Creating an instance of MQTT agent for subsribing/posting to the broker
    # brokerURL = "localhost"
    # brokerPort = 1883    # input("Enter the port number of the MQTT Broker: ")
    # agentName = input("Enter the name of the mqtt agent that will be created")


    # agent = mqtt.Client(agentName)
    # agent.on_connect = on_connect
    # agent.on_message = on_message
    # agent.connect(brokerURL, brokerPort)


    # agent.publish("architecture", serverNodesString)
    #agent.subscribe("Method_calls")
    #agent.subscribe("Subscribe")
    #agent.subscribe("Unsubscribe")





            
            
            

    # Opening the client's loop
    # with ThreadLoop() as tloop:
    #     with Client(serverUrl, tloop=tloop) as client:
    #         client.load_type_definitions()  # load definition of server specific structures/extension objects
    #         time.sleep(0.5)
    #         print("Objects node is: ", client.nodes.objects)
    #         #handle2 = subToVarID(client, "ns=2;s=controller1.m1.rotationalSpeed")
    #         #while True:
    #         embed()
    #
    # print("Check")

if __name__ == "__main__":
    main()











    
    
    
    
    


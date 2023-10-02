#!/usr/bin/python3
import sys
import os
import asyncio

import clientConfig
sys.path.insert(0, "..")
import logging
from pathlib import Path
import numpy as np
import json
from typing import List, Any
import paho.mqtt.client as mqtt
import codecs
import configparser
import threading
from opcUaClientClass import opcuaClient

########################################################################################################################
# For every client uses the following MQTT Topics:                                                                     #
# startStop:            Sending "startUp" on this topic, the system starts to operate all the clients for the servers  #
#                       registered at the clientData.ini file. Sending "stop" will stop all the client instances running #
# refreshClient:        Sending the number of the server you want to delete thread and create again                    #
# killClient:           Sending the number of the server whose client thread you want to kill                          #
# startClient:          Sending the number of the server you want to start a client thread for                         #
# initialize:           Sending a JSON string with the list of servers and arguments                                   #
# addServer:            Sending a JSON string with the list of arguments for the new server                            #
# editServer:           Sending a JSON string with the number of the server you want to edit and the list of arguments #
#                       for the new server                                                                             #
########################################################################################################################


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

clientsList = []    # List with the threads of all the client instances.

############################################################################
####                     DEFINING USEFUL FUNCTIONS                      ####
############################################################################

def startUp(numOfServers):
    kill = False
    # with ThreadPool() as pool:
    for i in range(0, numOfServers):
        print("In  startup loop")
        t = threading.Thread(target=startClient, args=(i,))
        print("One thread created")
        clientsList.append(t)
        clientsList[i].start()
        #startClient(i)
        print("Thread ", i, "has started")

def startClient(num):
    serversData = configparser.ConfigParser()
    serversData.read("clientData.ini")
    localurl = serversData.get('Server' + str(num), 'url')
    localname = serversData.get(('Server' + str(num)), 'name')
    localmqttUrl = serversData.get(('Server' + str(num)), 'mqtturl')
    localmqttPort = serversData.get('Server' + str(num), 'mqttport')
    localarchitectureTopic = serversData.get('Server' + str(num), 'architecturetopic')
    localconsoleTopic = serversData.get('Server' + str(num), 'consoletopic')
    localreadTopic = serversData.get('Server' + str(num), 'readtopic')
    localmethrequestTopic = serversData.get('Server' + str(num), 'methrequesttopic')
    localreadRequestTopic = serversData.get('Server' + str(num), 'readrequesttopic')
    localwriteRequestTopic = serversData.get('Server' + str(num), 'writerequesttopic')
    localsubrequestTopic = serversData.get('Server' + str(num), 'subrequesttopic')
    localunsubrequestTopic = serversData.get('Server' + str(num), 'unsubrequesttopic')
    localsubscribeTopic = serversData.get('Server' + str(num), 'subscriptiontopic')
    localconnectDisconnectTopic = serversData.get('Server' + str(num), 'connectdisconnecttopic')
    print("Where does this print?")
    with opcuaClient(localurl, localname, localmqttUrl, int(localmqttPort), localarchitectureTopic,
                     localconsoleTopic, localreadTopic, localmethrequestTopic, localreadRequestTopic,
                     localwriteRequestTopic, localsubrequestTopic, localunsubrequestTopic, localsubscribeTopic,
                     localconnectDisconnectTopic) as client:
        try:
            client.__enter__()
            print("Server with name " + str(client.name) + " detected")
            client.agent.publish("Server with name " + str(client.name) + " detected")
        except:
            print("Error occurred while trying to connect to server" + str(client.name) + "with url:" + str(
                client.url))
            client.agent.publish("Topic", "Error occurred while trying to connect to server" + str(
                client.name) + " with url: " + str(client.url))

        print("Inside the client ", num, "loop")
        tree = client.browse_server()
        treejs = json.dumps(tree)

        print(treejs)
        print("\n","\n")
        client.agent.publish('arc', "Connected with server"+"\n"+"\n")

        client.agent.publish('arc', treejs+"\n"+"\n")

        embed()

def stop(numOfServers):
    print("All client instances are terminated.")
    for i in range(0, numOfServers - 1):
        if clientsList[i].is_alive:
            clientsList[i].stop()

def killClient(num):
    clientsList[num]._stop()
    clientsList[num]._delete()


def refreshClient(num):
    killClient(num)
    startClient(num)


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
        elif msg.topic == "refreshClient":
            refreshClient(int(mess))
        elif msg.topic == "killClient":
            killClient(int(mess))
        elif msg.topic == "startClient":
            startClient(int(mess))
        elif msg.topic == "clearConfig":
            clientConfig.clearConfig()
        elif msg.topic == "addServer":
            clientConfig.addserver_from_UI(mess)
        elif msg.topic == "editServer":
            clientConfig.edit_server_from_UI(mess)



    generalAgent = mqtt.Client("general")
    generalAgent.on_connect = on_connect
    generalAgent.on_message = on_message
    generalAgent.connect(host="test.mosquitto.org", port=1883)
    generalAgent.subscribe("startStop")
    generalAgent.loop_forever()



if __name__ == "__main__":
    main()

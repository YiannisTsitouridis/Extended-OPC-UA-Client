#!/usr/bin/python3
import sys
import os
import asyncio
import time
import savedSubscriptionConfig
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
from asyncua.sync import ThreadLoop
from opcUaClientClass import opcuaClient

'''
For every client uses the following MQTT Topics:                                                                     
startStop:            Sending "startUp" on this topic, the system starts to operate all the clients for the servers  
                      registered at the clientData.ini file. Sending "stop" will stop all the client instances running
refreshClient:        Sending the number of the server you want to delete thread and create again                    
killClient:           Sending the number of the server whose client thread you want to kill                          
startClient:          Sending the number of the server you want to start a client thread for                         
initialize:           Sending a JSON string with the list of servers and arguments                                   
addServer:            Sending a JSON string with the list of arguments for the new server                            
editServer:           Sending a JSON string with the number of the server you want to edit and the list of arguments 
                      for the new server                                                                             
'''

# This part of code is for importing the appropriate console
try:
    from IPython import embed

    print("IPython module imported")
except ImportError:
    import code


clientsList = []  # List with the threads of all the client instances.
runningList = []  # List with booleans of the running condition of clients.


############################################################################
####                     DEFINING USEFUL FUNCTIONS                      ####
############################################################################

def runClientThread(num):
    createClientThread(num)
    clientsList[num].start()
    print("Thread " + str(num) + " started.")

def deleteServer(num):
    killClient(num)
    clientConfig.deleteServer(num)

def startClient(num):
    serversData = configparser.ConfigParser()
    serversData.read("clientData.ini")
    localurl = serversData.get('Server' + str(num), 'url')
    localtype = serversData.get(('Server' + str(num)), 'type')
    localname = serversData.get(('Server' + str(num)), 'name')
    localmqttUrl = serversData.get(('Server' + str(num)), 'mqtturl')
    localmqttPort = serversData.getint('Server' + str(num), 'mqttport')
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
    localCount = serversData.get('Server' + str(num), 'count')

    # Switching the client's running flag to True
    runningList[num] = True

    client = opcuaClient(localurl, localname, localtype, localmqttUrl, int(localmqttPort), localarchitectureTopic,
                     localconsoleTopic, localreadTopic, localmethrequestTopic, localreadRequestTopic,
                     localwriteRequestTopic, localsubrequestTopic, localunsubrequestTopic, localsubscribeTopic,
                     localconnectDisconnectTopic, localCount)
    mes = json.dumps({"message": "Server " + str(client.name) + " created"})
    client.agent.publish(client.consoleTopic, payload=mes)
    client.connect()
    print("Server with name " + str(client.name) + " connected")
    mes = json.dumps({"message": "Server " + str(client.name) + " connected"})
    client.agent.publish(client.consoleTopic, mes)
    print("Inside the client ", num, "loop")
    tree = client.browse_server()
    treejs = json.dumps(tree)
    print(treejs + "\n" + "\n")
    client.agent.publish(topic=client.architectureTopic, payload=treejs)
    client.make_saved_subscriptions()


    while runningList[num]:
        time.sleep(0.001)
    client.finish()
    client.disconnect()
    print("disconnected")


def stop(numOfServers):
    print("All client instances are terminated.")
    for i in range(0, numOfServers - 1):
        if clientsList[i].is_alive:
            clientsList[i].stop()

def createClientThread(i):
    t = threading.Thread(target=startClient, args=(i,))
    if i == len(clientsList):
        clientsList.append(t)
        runningList.append(False)
    elif i < len(clientsList):
        clientsList[i] = t
    else:
        print("Error with client threads numbering")


def remakeClientThread(i):
    clientsList[i] = threading.Thread(target=startClient, args=(i,))


def killClient(num):
    print("in killClient method")
    runningList[num] = False


############################################################################
####                     DEFINING MAIN FUNCTION                         ####
############################################################################
def main():
    logging.basicConfig(
        level=logging.INFO,  # Set the minimum level for messages to be recorded
        format='%(asctime)s [%(levelname)s]: %(message)s',  # Define the format of log messages
        handlers=[
            logging.StreamHandler()  # Send log messages to the console
        ]
    )

    def on_connect(agent, userdata, flags, rc):
        print("Connected!")

    def on_message(agent, userdata, msg):
        mess = str(msg.payload.decode("utf-8"))
        print("message recieved!")
        if msg.topic == "startStop":
            if mess == "stop":
                print("stop ordered")
                con = json.dumps({"message": "stop ordered"})
                generalAgent.publish("generalConsole", con)
                stop(maxNumOfServers)
            elif mess == "startUp":
                print("startUp ordered")
                # startUp(maxNumOfServers)
        elif msg.topic == "killClient":
            killClient(int(mess))
            con = json.dumps({"message": "Stopped Server" + str(mess)})
            generalAgent.publish('generalConsole', con)
        elif msg.topic == "startClient":
            runClientThread(int(mess))
            con = json.dumps({"message": "Server " + str(mess) + " started running"})
            generalAgent.publish("generalConsole", con)
        elif msg.topic == "clearConfig":
            clientConfig.cleanConfig()
        elif msg.topic == "addServer":
            feedback = clientConfig.addserver_from_UI(mess)
            fed = json.loads(feedback)
            count = fed["count"]
            createClientThread(count)
            print("Thread " + str(mess) + " created.")
            generalAgent.publish(feedtop, feedback)
        elif msg.topic == "editServer":
            if clientsList[mess].is_alive:
                print("This is a thread running, cannot edit.")
            else:
                clientConfig.edit_server_from_UI(mess)
                remakeClientThread(mess)
        elif msg.topic == "deleteServer":
            print("Delete message is ", mess)
            deleteServer(int(mess))

    file = configparser.ConfigParser()
    file.read("startingData.ini")
    host = file.get("BasicInfo", "host")
    port = file.getint("BasicInfo", "port")
    feedtop = file.get("BasicInfo", "feedbackTopic")
    generalAgent = mqtt.Client("general")
    generalAgent.on_connect = on_connect
    generalAgent.on_message = on_message
    generalAgent.connect(host=host, port=port)
    generalAgent.subscribe("startStop")
    generalAgent.subscribe("refreshClient")
    generalAgent.subscribe("killClient")
    generalAgent.subscribe("startClient")
    generalAgent.subscribe("clearConfig")
    generalAgent.subscribe("addServer")
    generalAgent.subscribe("editServer")
    generalAgent.subscribe("deleteServer")
    print("pass from here")
    serversData = configparser.ConfigParser()
    serversData.read("clientData.ini")
    maxNumOfServers = serversData.getint('maxNumberOfServers', 'serversNum')
    for a in (0, (maxNumOfServers - 1)):
        print("in here1")
        if serversData.has_section("Server" + str(a)):
            createClientThread(a)
            print("Thread " + str(a) + " created.")
        else:
            if a >= len(clientsList):
                clientsList.append(None)
                runningList.append(False)
            else:
                clientsList[a] = None
            clientsList[a] = None
    generalAgent.loop_forever()


if __name__ == "__main__":
    main()

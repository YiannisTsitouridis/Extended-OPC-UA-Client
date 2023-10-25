#!/usr/bin/python3
import sys
import configparser
import json



def giveCount(file):
    for i in (0, file.getint('NumberOfServers', 'serversNum')+1):
        if file.has_section("Server"+str(i)):
            pass
        else:
            return i
def addserver():
    initial_configfile = configparser.ConfigParser()
    initial_configfile.read("clientData.ini")

    # Updating the number of the servers value in the clientConfig.ini file #
    i = giveCount(initial_configfile)

    # Updating the number of the servers value in the clientConfig.ini file #
    initial_configfile.set('NumberOfServers', 'serversNum', i)
    initial_configfile.set('NumberOfServers', 'serversNum', str(i))

    # Taking console inputs for the new server. #
    serverUrl = input("Type the Url of the new server: ")
    serverName = input("Type the name of the new server: ")
    serverType = input("Type the type of the server: ")
    mqttUrl = input("Type the Url or username of the mqtt Broker: ")
    mqttPort = input("Type the port of the mqtt Broker: ")
    architectureTopic = input("Type the name of the architecture topic: ")
    consoleTopic = input("Type the topic for console messages: ")
    readTopic = input("Type the topic for the read values: ")
    methRequestTopic = input("Type the topic for method requests: ")
    readRequestTopic = input("Type the topic for reading values requests: ")
    writeRequestTopic = input("Type the topic for writing values requests: ")
    subRequestTopic = input("Type the topic for variable subscription requests: ")
    unSubRequestTopic = input("unsubscribe request topic: ")
    subscriptionTopic = input("Subscription Topic: ")
    connectDisconnectTopic = input("Connect-Disconnect Topic: ")


    # Setting the taken inputs in the clientConfig.ini file, in the new server's section. #
    initial_configfile.add_section("Server" + str(i))
    initial_configfile.set('Server' + str(i), 'url', serverUrl)
    initial_configfile.set('Server' + str(i), 'name', serverName)
    initial_configfile.set('Server' + str(i), 'type', serverType)
    initial_configfile.set('Server' + str(i), 'mqtturl', mqttUrl)
    initial_configfile.set('Server' + str(i), 'mqttport', mqttPort)
    initial_configfile.set('Server' + str(i), 'architecturetopic', architectureTopic)
    initial_configfile.set('Server' + str(i), 'consoletopic', consoleTopic)
    initial_configfile.set('Server' + str(i), 'readtopic', readTopic)
    initial_configfile.set('Server' + str(i), 'methrequesttopic', methRequestTopic)
    initial_configfile.set('Server' + str(i), 'readrequesttopic', readRequestTopic)
    initial_configfile.set('Server' + str(i), 'writerequesttopic', writeRequestTopic)
    initial_configfile.set('Server' + str(i), 'subrequesttopic', subRequestTopic)
    initial_configfile.set('Server' + str(i), 'unsubrequesttopic', unSubRequestTopic)
    initial_configfile.set('Server' + str(i), 'subscriptiontopic', subscriptionTopic)
    initial_configfile.set('Server' + str(i), 'connectdisconnecttopic', connectDisconnectTopic)

    with open(r"clientData.ini", 'w') as configfile:
        initial_configfile.write(configfile)

    return i
    # HERE we must find a way to create the thread
def edit_server(num):
    initial_configfile = configparser.ConfigParser()
    initial_configfile.read("clientData.ini")

    # Taking console inputs for the new server. #
    serverUrl = input("Type the new Url of the server: ")
    serverName = input("Type the new name of the new server: ")
    serverType = input("Type the type of the server: ")
    mqttUrl = input("Type the new Url or username of the mqtt Broker: ")
    mqttPort = input("Type the new port of the mqtt Broker: ")
    architectureTopic = input("Type the new name of the architecture topic: ")
    consoleTopic = input("Type the new topic for console messages: ")
    readTopic = input("Type the new topic for the read values: ")
    methRequestTopic = input("Type the new topic for method requests: ")
    readRequestTopic = input("Type the new topic for reading values requests: ")
    writeRequestTopic = input("Type the new topic for writing values requests: ")
    subRequestTopic = input("Type the new topic for variable subscription requests: ")
    unSubRequestTopic = input("New Unsubscribe request topic: ")
    subscriptionTopic = input("New Subscription Topic: ")
    connectDisconnectTopic = input("New Connect-Disconnect Topic: ")

    # Setting the taken inputs in the clientConfig.ini file, in the new server's section. #
    initial_configfile.set('Server' + str(num), 'url', serverUrl)
    initial_configfile.set('Server' + str(num), 'name', serverName)
    initial_configfile.set('Server' + str(num), 'type', serverType)
    initial_configfile.set('Server' + str(num), 'mqtturl', mqttUrl)
    initial_configfile.set('Server' + str(num), 'mqttport', mqttPort)
    initial_configfile.set('Server' + str(num), 'architecturetopic', architectureTopic)
    initial_configfile.set('Server' + str(num), 'consoletopic', consoleTopic)
    initial_configfile.set('Server' + str(num), 'readtopic', readTopic)
    initial_configfile.set('Server' + str(num), 'methrequesttopic', methRequestTopic)
    initial_configfile.set('Server' + str(num), 'readrequesttopic', readRequestTopic)
    initial_configfile.set('Server' + str(num), 'writerequesttopic', writeRequestTopic)
    initial_configfile.set('Server' + str(num), 'subrequesttopic', subRequestTopic)
    initial_configfile.set('Server' + str(num), 'unsubrequesttopic', unSubRequestTopic)
    initial_configfile.set('Server' + str(num), 'subscriptiontopic', subscriptionTopic)
    initial_configfile.set('Server' + str(num), 'connectdisconnecttopic', connectDisconnectTopic)

    with open(r"clientData.ini", 'w') as configfile:
        initial_configfile.write(configfile)


def addserver_from_UI(dataFromUI):

    dataObject = json.loads(dataFromUI)

    initial_configfile = configparser.ConfigParser()
    initial_configfile.read("clientData.ini")

    i = giveCount(initial_configfile)

    num = initial_configfile.getint('NumberOfServers','serversNum')
    # Updating the number of the servers value in the clientConfig.ini file #
    initial_configfile.set('NumberOfServers', 'serversNum', str(num+1))

    # Taking console inputs for the new server. #
    serverUrl = dataObject["serverUrl"]
    serverName = dataObject["serverName"]
    serverType = dataObject["serverType"]
    mqttUrl = dataObject["mqttUrl"]
    mqttPort = dataObject["mqttPort"]
    architectureTopic = dataObject["architectureTopic"]
    consoleTopic = dataObject["consoleTopic"]
    readTopic = dataObject["readTopic"]
    methRequestTopic = dataObject["methRequestTopic"]
    readRequestTopic = dataObject["readRequestTopic"]
    writeRequestTopic = dataObject["writeRequestTopic"]
    subRequestTopic = dataObject["subRequestTopic"]
    unSubRequestTopic = dataObject["unSubRequestTopic"]
    subscriptionTopic = dataObject["subscriptionTopic"]
    connectDisconnectTopic = dataObject["connectDisconnectTopic"]

    # Setting the taken inputs in the clientConfig.ini file, in the new server's section. #
    initial_configfile.add_section("Server" + str(i))
    initial_configfile.set('Server' + str(i), 'url', serverUrl)
    initial_configfile.set('Server' + str(i), 'name', serverName)
    initial_configfile.set('Server' + str(i), 'type', serverType)
    initial_configfile.set('Server' + str(i), 'mqtturl', mqttUrl)
    initial_configfile.set('Server' + str(i), 'mqttport', str(mqttPort))
    initial_configfile.set('Server' + str(i), 'architecturetopic', architectureTopic)
    initial_configfile.set('Server' + str(i), 'consoletopic', consoleTopic)
    initial_configfile.set('Server' + str(i), 'readtopic', readTopic)
    initial_configfile.set('Server' + str(i), 'methrequesttopic', methRequestTopic)
    initial_configfile.set('Server' + str(i), 'readrequesttopic', readRequestTopic)
    initial_configfile.set('Server' + str(i), 'writerequesttopic', writeRequestTopic)
    initial_configfile.set('Server' + str(i), 'subrequesttopic', subRequestTopic)
    initial_configfile.set('Server' + str(i), 'unsubrequesttopic', unSubRequestTopic)
    initial_configfile.set('Server' + str(i), 'subscriptiontopic', subscriptionTopic)
    initial_configfile.set('Server' + str(i), 'connectdisconnecttopic', connectDisconnectTopic)

    with open(r"clientData.ini", 'w') as configfile:
        initial_configfile.write(configfile)
    splt = architectureTopic.split('/')
    uuid = splt[1]
    fed = {"serveruuid": uuid, "count": i}
    feedback = json.dumps(fed)
    return feedback

def edit_server_from_UI(dataFromUI):
    dataObject = json.loads(dataFromUI)
    initial_configfile = configparser.ConfigParser()
    initial_configfile.read("clientData.ini")
    i = dataObject["numOfServer"]

    serverUrl = dataObject["serverUrl"]
    serverName = dataObject["serverName"]
    serverType = dataObject["serverType"]
    mqttUrl = dataObject["mqttUrl"]
    mqttPort = dataObject["mqttPort"]
    architectureTopic = dataObject["architectureTopic"]
    consoleTopic = dataObject["consoleTopic"]
    readTopic = dataObject["readTopic"]
    methRequestTopic = dataObject["methRequestTopic"]
    readRequestTopic = dataObject["readRequestTopic"]
    writeRequestTopic = dataObject["writeRequestTopic"]
    subRequestTopic = dataObject["subRequestTopic"]
    unSubRequestTopic = dataObject["unSubRequestTopic"]
    subscriptionTopic = dataObject["subscriptionTopic"]
    connectDisconnectTopic = dataObject["connectDisconnectTopic"]

    initial_configfile.set('Server' + str(i), 'url', serverUrl)
    initial_configfile.set('Server' + str(i), 'name', serverName)
    initial_configfile.set('Server' + str(i), 'type', serverType)
    initial_configfile.set('Server' + str(i), 'mqtturl', mqttUrl)
    initial_configfile.set('Server' + str(i), 'mqttport', mqttPort)
    initial_configfile.set('Server' + str(i), 'architecturetopic', architectureTopic)
    initial_configfile.set('Server' + str(i), 'consoletopic', consoleTopic)
    initial_configfile.set('Server' + str(i), 'readtopic', readTopic)
    initial_configfile.set('Server' + str(i), 'methrequesttopic', methRequestTopic)
    initial_configfile.set('Server' + str(i), 'readrequesttopic', readRequestTopic)
    initial_configfile.set('Server' + str(i), 'writerequesttopic', writeRequestTopic)
    initial_configfile.set('Server' + str(i), 'subrequesttopic', subRequestTopic)
    initial_configfile.set('Server' + str(i), 'unsubrequesttopic', unSubRequestTopic)
    initial_configfile.set('Server' + str(i), 'subscriptiontopic', subscriptionTopic)
    initial_configfile.set('Server' + str(i), 'connectdisconnecttopic', connectDisconnectTopic)


def deleteServer(i):
    initial_configfile = configparser.ConfigParser()
    initial_configfile.read("clientData.ini")

    initial_configfile.remove_section('Server'+str(i))

    with open(r"clientData.ini", 'w') as configfile:
        initial_configfile.write(configfile)

def cleanConfig():
    initial_configfile = configparser.ConfigParser()
    initial_configfile.read("clientData.ini")
    num = initial_configfile.getint('NumberOfServers', 'serversNum')
    for i in range(0, num):
        initial_configfile.remove_section('Server' + str(i))
    initial_configfile.set('NumberOfServers', 'serversNum', '0')

    with open(r"clientData.ini", 'w') as configfile:
        initial_configfile.write(configfile)

def deleteAll():
    pass

if __name__=='__main__':
    args = sys.argv
    # if len(args)
    function_name = args[1]
    if args:
        if function_name == addserver_from_UI.__name__:
            addserver_from_UI(args[2])
        elif function_name == edit_server_from_UI.__name__:
            edit_server_from_UI(args[2])
        elif function_name == cleanConfig().__name__:
            cleanConfig()
        else:
            print("Invalid function name.")

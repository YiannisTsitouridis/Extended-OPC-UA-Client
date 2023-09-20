#!/usr/bin/python3
import sys
import configparser
import json

def addserver():
    initial_configfile = configparser.ConfigParser()
    initial_configfile.read("clientData.ini")

    # Updating the number of the servers value in the clientConfig.ini file #
    numOfServers = initial_configfile.getint('NumberOfServers', 'serversNum')
    newNumOfServers = numOfServers + 1
    initial_configfile.set('NumberOfServers', 'serversNum', str(newNumOfServers))

    # Taking console inputs for the new server. #
    serverUrl = input("Type the Url of the new server: ")
    serverName = input("Type the name of the new server: ")
    mqttUrl = input("Type the Url or username of the mqtt Broker: ")
    mqttPort = input("Type the port of the mqtt Broker: ")
    architectureTopic = input("Type the name of the architecture topic: ")
    consoleTopic = input("Type the topic for console messages: ")
    readTopic = input("Type the topic for the read values: ")
    methRequestTopic = input("Type the topic for method requests: ")
    readRequestTopic = input("Type the topic for reading values requests: ")
    writeRequestTopic = input("Type the topic for writing values requests: ")
    subRequestTopic = input("Type the topic for variable subscription requests: ")
    unSubRequestTopic = input("unsubscribe request topic")
    subscriptionTopic = input("Subscription Topic")

    # Setting the taken inputs in the clientConfig.ini file, in the new server's section. #
    initial_configfile.add_section("Server" + str(numOfServers))
    initial_configfile.set('Server' + str(numOfServers), 'serversNum', serverUrl)
    initial_configfile.set('Server' + str(numOfServers), 'serverName', serverName)
    initial_configfile.set('Server' + str(numOfServers), 'mqttUrl', mqttUrl)
    initial_configfile.set('Server' + str(numOfServers), 'mqttPort', mqttPort)
    initial_configfile.set('Server' + str(numOfServers), 'architectureTopic', architectureTopic)
    initial_configfile.set('Server' + str(numOfServers), 'consoleTopic', consoleTopic)
    initial_configfile.set('Server' + str(numOfServers), 'readTopic', readTopic)
    initial_configfile.set('Server' + str(numOfServers), 'methRequestTopic', methRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'readRequestTopic', readRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'writeRequestTopic', writeRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'subRequestTopic', subRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'unSubRequestTopic', unSubRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'subscriptionTopic', subscriptionTopic)


    with open(r"try.ini", 'w') as configfile:
        initial_configfile.write(configfile)


def initialize():
    config = configparser.ConfigParser()

    n = int(input("Number of servers: "))

    config.add_section('NumberOfServers')
    config.set('NumberOfServers', 'serversNum', str(n))

    for i in range(0, n):
        config.add_section("Server" + str(i))

        # Taking console inputs for every server. #
        serverUrl = input("Type the Url of server "+str(i)+": ")
        serverName = input("Type the name of server " + str(i) + ": ")
        mqttUrl = input("Type the url of mqtt Broker " + str(i) + ": ")
        mqttPort = input("Type the port of mqtt Broker " + str(i) + ": ")
        architectureTopic = input("Type the topic where the server" + str(i) + " architecture will be sent: ")
        consoleTopic = input("Type the topic for the console messages of server" + str(i) + ": ")
        readTopic = input("Type the topic for displaying the values ordered to read from server" + str(i) + ": ")
        methRequestTopic = input("method request topic for server" + str(i))
        readRequestTopic = input("read request topic for server" + str(i))
        writeRequestTopic = input("write request topic for server" + str(i))
        subRequestTopic = input("subscription request topic for server" + str(i))
        unSubRequestTopic = input("unsubscribe request topic for server" + str(i))
        subscriptionTopic = input("Subscription Topic for server" + str(i))

        # Setting the taken inputs in the clientConfig.ini file #
        config.set('Server' + str(i), 'url', serverUrl)
        config.set('Server' + str(i), 'name', serverName)
        config.set('Server' + str(i), 'mqttUrl', mqttUrl)
        config.set('Server' + str(i), 'mqttPort', mqttPort)
        config.set('Server' + str(i), 'architectureTopic', architectureTopic)
        config.set('Server' + str(i), 'consoleTopic', consoleTopic)
        config.set('Server' + str(i), 'readTopic', readTopic)
        config.set('Server' + str(i), 'methRequestTopic', methRequestTopic)
        config.set('Server' + str(i), 'readRequestTopic', readRequestTopic)
        config.set('Server' + str(i), 'writeRequestTopic', writeRequestTopic)
        config.set('Server' + str(i), 'subRequestTopic', subRequestTopic)
        config.set('Server' + str(i), 'unSubRequestTopic', unSubRequestTopic)
        config.set('Server' + str(i), 'subscriptionTopic', subscriptionTopic)

    with open(r"clientData.ini", 'w') as configfile:
        config.write(configfile)


def addserver_from_UI(dataFromUI):

    dataObject = json.loads(dataFromUI)

    initial_configfile = configparser.ConfigParser()
    initial_configfile.read("clientData.ini")

    # Updating the number of the servers value in the clientConfig.ini file #
    numOfServers = initial_configfile.getint('NumberOfServers', 'serversNum')
    newNumOfServers = numOfServers + 1
    initial_configfile.set('NumberOfServers', 'serversNum', newNumOfServers)

    # Taking console inputs for the new server. #
    serverUrl = dataObject["serverUrl"]
    serverName = dataObject["serverName"]
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

    # Setting the taken inputs in the clientConfig.ini file, in the new server's section. #
    initial_configfile.add_section("Server" + str(numOfServers))
    initial_configfile.set('Server' + str(numOfServers), 'serversNum', serverUrl)
    initial_configfile.set('Server' + str(numOfServers), 'serverName', serverName)
    initial_configfile.set('Server' + str(numOfServers), 'mqttUrl', mqttUrl)
    initial_configfile.set('Server' + str(numOfServers), 'mqttPort', mqttPort)
    initial_configfile.set('Server' + str(numOfServers), 'architectureTopic', architectureTopic)
    initial_configfile.set('Server' + str(numOfServers), 'consoleTopic', consoleTopic)
    initial_configfile.set('Server' + str(numOfServers), 'readTopic', readTopic)
    initial_configfile.set('Server' + str(numOfServers), 'methRequestTopic', methRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'readRequestTopic', readRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'writeRequestTopic', writeRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'subRequestTopic', subRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'unSubRequestTopic', unSubRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'subscriptionTopic', subscriptionTopic)



def initialize_from_UI(dataFromUI):

    dataObject = json.loads(dataFromUI)

    config = configparser.ConfigParser()

    n = len(dataObject)

    config.add_section('NumberOfServers')
    config.set('NumberOfServers', 'serversNum', str(n))

    for i in range(0, n):
        config.add_section("Server" + str(i))

        # Taking console inputs for every server. #
        serverUrl = dataObject["serverUrl"]
        serverName = dataObject["serverName"]
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

        # Setting the taken inputs in the clientConfig.ini file #
        config.set('Server' + str(i), 'url', serverUrl)
        config.set('Server' + str(i), 'name', serverName)
        config.set('Server' + str(i), 'mqttUrl', mqttUrl)
        config.set('Server' + str(i), 'mqttPort', mqttPort)
        config.set('Server' + str(i), 'architectureTopic', architectureTopic)
        config.set('Server' + str(i), 'consoleTopic', consoleTopic)
        config.set('Server' + str(i), 'readTopic', readTopic)
        config.set('Server' + str(i), 'methRequestTopic', methRequestTopic)
        config.set('Server' + str(i), 'readRequestTopic', readRequestTopic)
        config.set('Server' + str(i), 'writeRequestTopic', writeRequestTopic)
        config.set('Server' + str(i), 'subRequestTopic', subRequestTopic)
        config.set('Server' + str(i), 'unSubRequestTopic', unSubRequestTopic)
        config.set('Server' + str(i), 'subscriptionTopic', subscriptionTopic)

    with open(r"clientData.ini", 'w') as configfile:
        config.write(configfile)


    # def deleteServer():
    # def deleteServer_from_UI():


if __name__=='__main__':
    args = sys.argv
    # if len(args)
    function_name = args[1]
    if args:
        if function_name == initialize.__name__:
            initialize()
        elif function_name == addserver.__name__:
            addserver()
        elif function_name == addserver_from_UI.__name__:
            addserver_from_UI(args[2])
        elif function_name == initialize_from_UI.__name__:
            initialize_from_UI(args[2])
        else:
            print("Invalid function name.")

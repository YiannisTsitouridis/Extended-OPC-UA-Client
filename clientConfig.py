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
    initial_configfile.set('NumberOfServers', 'serversNum', newNumOfServers)

    # Taking console inputs for the new server. #
    serverUrl = input("Type the Url of the new server ")
    serverName = input("Type the name of the new server: ")
    mqttUrl = input("Type the name of the new server: ")
    mqttPort = input("Type the name of the new server: ")
    architectureTopic = input("Type the name of the new server: ")
    consoleTopic = input("Type the name of the new server: ")
    readTopic = input("Type the name of the new server: ")
    methRequestTopic = input("method request topic")
    readRequestTopic = input("read request topic")
    writeRequestTopic = input("write request topic")
    subRequestTopic = input("subscription request topic")
    unSubRequestTopic = input("unsubscribe request topic")

    # Setting the taken inputs in the clientConfig.ini file, in the new server's section. #
    initial_configfile.add_section("Server" + str(numOfServers))
    initial_configfile.set('Server', 'serversNum', serverUrl)
    initial_configfile.set('Server', 'serverName', serverName)
    initial_configfile.set('Server', 'mqttUrl', mqttUrl)
    initial_configfile.set('Server', 'mqttPort', mqttPort)
    initial_configfile.set('Server', 'architectureTopic', architectureTopic)
    initial_configfile.set('Server', 'consoleTopic', consoleTopic)
    initial_configfile.set('Server', 'readTopic', readTopic)
    initial_configfile.set('Server' + str(numOfServers), 'methRequestTopic', methRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'readRequestTopic', readRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'writeRequestTopic', writeRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'subRequestTopic', subRequestTopic)
    initial_configfile.set('Server' + str(numOfServers), 'unSubRequestTopic', unSubRequestTopic)

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
        architectureTopic = input("Type the topic where the server architecture will be sent" + str(i) + ": ")
        consoleTopic = input("Type the topic for the console messages " + str(i) + ": ")
        readTopic = input("Type the topic for displaying the values ordered to read " + str(i) + ": ")
        methRequestTopic = input("method request topic")
        readRequestTopic = input("read request topic")
        writeRequestTopic = input("write request topic")
        subRequestTopic = input("subscription request topic")
        unSubRequestTopic = input("unsubscribe request topic")
        subscriptionTopic = input("Subscription Topic")

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

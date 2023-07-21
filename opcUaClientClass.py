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


# For every server in the industry another client entity should be created to be connected with it
# url: the url of the server that each client will connect to
# name:the name of each client

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

class opcuaClient(Client):
    # This class is a child class to the Client Class from asyncua package.
    # When you add the __init__() function, the child class will no longer inherit the parent's __init__() function.
    # Unless you run the super().__init__ function
    def __init__(self, url: str, name: str, mqtturl: str, mqttport: int, architecturetopic: str, consoletopic: str, readtopic: str):
        super().__init__(url)
        self.name = name
        self.brokerURL = mqtturl
        self.brokerPort = mqttport
        time.sleep(2)
        self.architectureTopic = architecturetopic
        self.consoleTopic = consoletopic
        self.readTopic = readtopic

        self.agent = self.createMqttAgent()
        self.initial_subscriptions()

        print(self.name)
        print(self.consoleTopic)
        print(self.readTopic, self.brokerURL, self.brokerPort)


    def createMqttAgent(self):
        def on_connect(agent, userdata, flags, rc):
            if rc == 0:
                print("Agent connected OK")
            else:
                print("Bad agent connection to MQTT Broker with result code " + str(rc))
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.

        def on_message(agent, userdata, msg):
            print(msg.topic + " " + str(msg.payload))
            logging.basicConfig(level=logging.WARN)
            # logger = logging.getLogger("KeepAlive")
            # logger.setLevel(logging.DEBUG)

            if (msg.topic == str(self.name) + "/Method_calls"):
                mess = json.loads(msg.payload)
                print("Call of method", mess["methodID"], " was ordered.")
                agent.publish(str(self.consoleTopic), "Call of method " + mess["methodID"] + " was ordered.")
                if len(mess) == 1:
                    callMeth = self.callMethodFromNodeID(mess["methodID", self])
                    return callMeth
                elif len(mess) == 2:
                    callMeth = self.callMethodFromNodeID(mess["methodID"], self, mess["arg1"])
                    return callMeth
                elif len(mess) == 3:
                    callMeth = self.callMethodFromNodeID(mess["methodID"], self, mess["arg1"], mess["arg1"])
                    return callMeth

            if (msg.topic == str(self.name) + "/Subscribe"):
                print("we've got something here")
                mess = json.loads(msg.payload)
                mesg = str(msg.payload.decode("utf-8"))
                print("Subscription on the variable " + mesg + " was ordered.")
                agent.publish(self.consoleTopic, "Subscription on the variable " + mesg + " was ordered.")
                subvar = self.subToVarID(mess["varID"], mess["SubscriptionPeriod"])
                return subvar

            if (msg.topic == str(self.name) + "/Unsubscribe"):
                mess = str(msg.payload.decode("utf-8"))
                unsu = self.unsubFromVarID(mess)
                print("Ending subscription on the variable ", mess, " was ordered.")
                agent.publish(self.consoleTopic, "Ending subscription on the variable " + mess + " was ordered.")

            if (msg.topic == str(self.name) + "/Read"):
                mess = msg.payload
                value = self.readValue(mess)
                agent.publish(self.readTopic, value)
                return value

            if (msg.payload == str(self.name) + "/Write"):
                mess = json.loads(msg.payload)
                if len(mess) != 2:
                    agent.publish(self.consoleTopic, "Wrong number of arguements")
                    return "Wrong number of arguements"
                else:
                    var = self.get_node(mess["varID"])
                    var.set_value(mess["value"])

        self.agent = mqtt.Client(self.name)
        print("Here?")
        self.agent.on_connect = on_connect
        print("or here?")
        self.agent.on_message = on_message
        self.agent.connect(host=self.brokerURL)
        self.agent.loop_start()
        time.sleep(2)

        return self.agent

    def initial_subscriptions(self):
        # From the birth of mqtt agent, we want it to subscribe to the following topics.
        self.agent.subscribe(self.consoleTopic)
        self.agent.subscribe(self.readTopic)
        self.agent.subscribe(str(self.name) + "/Subscribe")
        self.agent.subscribe(str(self.name) + "/Method_calls")
        self.agent.subscribe(str(self.name) + "/Unsubscribe")
        return 0




    def __str__(self):
        return f"{self.name} with url :{self.url} and tloop = {self.tloop}"



    def browse_node_tree(self, node):
        """
        Build and return a nested node tree dict by recursion (filtered by OPC UA objects and variables).
        """
        node_class = node.read_node_class()
        children = []
        for child in node.get_children():
            if child.read_node_class() in [ua.NodeClass.Object, ua.NodeClass.Variable, ua.NodeClass.Method, ua.NodeClass.ObjectType]:
                children.append(
                    self.browse_node_tree(child)
                )
        if node_class != ua.NodeClass.Variable:
            var_type = None
        else:
            try:
                var_type = (node.read_data_type_as_variant_type()).value
            except ua.UaError:
                _logger.warning('Node Variable Type could not be determined for %r', node)
                var_type = None
        return {
            'id': node.nodeid.to_string(),
            'name': (node.read_display_name()).Text,
            'cls': node_class.value,
            'children': children,
            'type': var_type,
        }

    def browse_server(self):
        """
        Build and return a nested node tree dict by recursion (filtered by OPC UA objects and variables).
        And bring back the architecture of each server.
        """
        return self.browse_node_tree(self.get_root_node())



    # Defining the dynamic list for the IDs of the variables that are to be subscribed.
    subVarIDList: list[str] = []
    subscriptionsList: list[object] = []

    def readValue(self, varID):
        try:
            var = self.get_node(varID)
            ret = var.read_value()
            return ret
        except:
            print("Couldn't read the value with ID ", varID)

    class SubHandler(object):
        """
        Subscription Handler. To receive events from server for a subscription
        data_change and event methods are called directly from receiving thread.
        Do not do expensive, slow or network operation there. Create another
        thread if you need to do such a thing
        """

        def datachange_notification(self, node, val):
            print("Python: New data change event", node, val)

        def event_notification(self, event):
            print("Python: New event", event)

    def subToVarID(self, varID, freq):
        agent = self.agent
        class SubHandler2(opcuaClient.SubHandler):
            """
            Subscription Handler. To receive events from server for a subscription
            data_change and event methods are called directly from receiving thread.
            Do not do expensive, slow or network operation there. Create another
            thread if you need to do such a thing
            """

            def datachange_notification(self, node, val):
                print("Python: New data change event", node, val)
                agent.publish(topic="subscribe", payload=str(val))

                # opcuaClient.handlerPost(node, val)

            def event_notification(self, event):
                print("Python: New event", event)

        if varID in self.subVarIDList:
            print("There is a subscription to the variable " + varID + " already.")
            self.agent.publish(self.consoleTopic, "There is a subscription to the variable " + varID + " already.")
        else:
            var = self.get_node(varID)
            handler = self.SubHandler
            sub = self.create_subscription(freq, handler)  # First arguement here is period and determines the frequency of checking for data.
            handle = sub.subscribe_data_change(var)

            self.subscriptionsList.append(sub)
            self.subVarIDList.append(varID)
            print("Subscription on the variable ", varID, " successful.")
            self.agent.publish(self.consoleTopic, "Subscription on the variable " + varID + "successful.")
            return sub

    def unsubFromVarID(self, varID):
        if varID in self.subVarIDList:
            ind = self.subVarIDList.index(varID)
            sub = self.subscriptionsList[ind]
            sub.delete()
            del self.subscriptionsList[ind]
            del self.subVarIDList[ind]
            print("Ending subscription on the variable ", varID, " successfully.")
            return "Ending subscription on the variable ", varID, " successfully."
        else:
            print("No subscription found to the variable ", varID, ".")
            self.agent.publish(str(self.name) + "/ex/client", "No subscription found to the variable " + varID + ".")
            return "No subscription found to the variable ", varID, "."

    def callMethodFromNodeID(self, nodeId, *args):
        meth = self.get_node(nodeId)
        print("Method with Browse Name ", str(meth.read_browse_name), "is being called")
        try:
            methodParent: object = meth.get_parent()
        except:
            print("Could not find the parent of the method with ID: ", nodeId)
            self.agent.publish(str(self.name) + "/ex/client", "Could not find the parent of the method with ID: " + nodeId)
        result = methodParent.call_method(meth, *args)
        return result

    def handlerPost(self, node, val):
        self.agent.publish(node, val)




def main():
    serversData = configparser.ConfigParser()
    serversData.read("clientData.ini")
    numOfServers = serversData.getint('NumberOfServers', 'serversNum')
    clientsList = []
    for i in range(1, numOfServers + 1):
        with ThreadLoop() as tloop:
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
                # print(client.name, " architecture posted:" + "\n \n", tree)
                # print("hello!")
                # client.agent.loop_start()
                # client.agent.subscribe("hotel")
                embed()
            print("reach here")
    print("Reach here!!!!!!")
if __name__ == "__main__":
    main()
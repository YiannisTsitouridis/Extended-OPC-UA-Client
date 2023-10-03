import sys
sys.path.insert(0, "..")
import logging
import time
from pathlib import Path
import numpy as np
import json
from asyncua import ua, common, sync, Client
from asyncua.sync import DataTypeDictionaryBuilder
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, tostring
from dict2xml import dict2xml
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
import paho.mqtt.client as mqtt
from asyncua.sync import Client, ThreadLoop, _logger


###########################################################################################################################
# For every server in the industry another client entity should be created to be connected with it                        #
# url:                    the url of the server that each client will connect to                                          #
# name:                   the name of each client(same as the server name)                                                #
# mqtturl:                the url/name of the mqtt broker through which the data are transferred to/from the Platform     #
# mqttport:               the port of the mqtt broker through which the data are transferred to/from the Platform         #
# architecturetopic:      the mqtt topic in which the nodes of the server will be posted after connecting to it           #
# consoletopic:           the mqtt topic where console-type messages are posted                                           #
# readtopic:              the mqtt topic where the read-asked values are published                                        #
# methRequestTopic:       the mqtt topic where the UI publishes to call an OPC UA method                                  #
# readRequestTopic:       the mqtt topic where the UI publishes to request to read the value of a variable                #
# writeRequestTopic:      the mqtt topic where the UI publishes to request to write the value of a variable               #
# subRequestTopic:        the mqtt topic where the UI publishes to request to monitor the value changes of a variable     #
# unSubRequestTopic:      the mqtt topic where the UI publishes to request to stop monitoring variable's value changes    #
# connectDisconnectTopic: the mqtt topic where the UI publishes to request to stop monitoring variable's value changes    #
###########################################################################################################################
class opcuaClient(Client):
    # This class is a child class to the Client Class from asyncua package.
    # When you add the __init__() function, the child class will no longer inherit the parent's __init__() function.
    # Unless you run the super().__init__ function
    def __init__(self, url: str, name: str, type: str, mqtturl: str, mqttport: int, architecturetopic: str, consoletopic: str,
                 readtopic: str, methRequestTopic: str, readRequestTopic: str, writeRequestTopic: str,
                 subRequestTopic: str, unSubRequestTopic:str, subscribeTopic:str, connectDisconnectTopic:str):
        super().__init__(url)
        self.name = name
        self.type = type
        self.brokerURL = mqtturl
        self.brokerPort = mqttport
        time.sleep(2)
        self.architectureTopic = architecturetopic
        self.consoleTopic = consoletopic
        self.readTopic = readtopic
        self.methRequestTopic = methRequestTopic
        self.readRequestTopic = readRequestTopic
        self.writeRequestTopic = writeRequestTopic
        self.subRequestTopic = subRequestTopic
        self.unSubRequestTopic = unSubRequestTopic
        self.subscribeTopic = subscribeTopic
        self.connectDisconnectTopic = connectDisconnectTopic
        # TO DO!
        # Add fields that have to do with server's security policy.
        # TO DO!
        # Add field for the server implementation.
        # self.set_security(policy = , certificate = , private_key = , private_key_password = , server_certificate = , mode = )
        self.agent:mqtt.Client = self.createMqttAgent()
        self.initial_subscriptions()

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

            if (msg.topic == self.methRequestTopic):
                mess = json.loads(msg.payload)
                print("Call of method", mess["methodID"], " was ordered.")
                agent.publish(str(self.consoleTopic), "Call of method " + mess["methodID"] + " was ordered.")
                if len(mess) == 1:
                    callMeth = self.callMethodFromNodeID(mess["methodID"])
                elif len(mess) == 2:
                    self.callMethodFromNodeID(mess["methodID"], mess["arg1"])
                elif len(mess) == 3:
                    callMeth = self.callMethodFromNodeID(str(mess["methodID"]), mess["arg1"], mess["arg2"])

            if (msg.topic == self.subRequestTopic):
                print("we've got something here")
                mess = json.loads(msg.payload)
                mesg = str(msg.payload.decode("utf-8"))
                print("Subscription on the variable " + mesg + " was ordered.")
                agent.publish(str(self.consoleTopic), "Subscription on the variable " + mesg + " was ordered.")
                subvar = self.subToVarID(mess["varID"], mess["SubscriptionPeriod"], self.subscribeTopic)
                return subvar

            if (msg.topic == self.unSubRequestTopic):
                mess = str(msg.payload.decode("utf-8"))
                unsu = self.unsubFromVarID(mess)
                print("Ending subscription on the variable ", mess, " was ordered.")
                agent.publish(self.consoleTopic, "Ending subscription on the variable " + mess + " was ordered.")

            if (msg.topic == self.readRequestTopic):
                mess = str(msg.payload.decode("utf-8"))
                retMess = self.readValue(mess)
                agent.publish(self.readTopic, retMess)
                return retMess

            if (msg.topic == self.writeRequestTopic):
                mess = json.loads(msg.payload)
                if len(mess) != 2:
                    agent.publish(self.consoleTopic, "Wrong number of arguements")
                    print("Wrong number of arguements")
                    return "Wrong number of arguements"
                else:
                    var = self.get_node(mess["varID"])
                    var.set_value(mess["value"])
                    print("var written")

            if (msg.topic == self.connectDisconnectTopic):
                mess = str(msg.payload.decode("utf-8"))
                if mess == "disconnect":
                    self.disconnect()
                elif mess == "reconnect":
                    self.connect()

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
        self.agent.subscribe(str(self.name) + "/Subscribe")
        self.agent.subscribe(str(self.name) + "/Method_calls")
        self.agent.subscribe(str(self.name) + "/Unsubscribe")
        self.agent.subscribe(str(self.name) + "/Read")
        self.agent.subscribe(str(self.name) + "/Write")

        return 0

    def __str__(self):
        return f"{self.name} with url :{self.name} and tloop = {self.tloop}"

    # Defining the dynamic list for the IDs of the variables that are to be subscribed.
    subVarIDList: list[str] = []
    subscriptionsList: list[object] = []

    def subToVarID(self, varID, period, Topic):

        agent = self.agent
        class SubHandler(object):
            """
            Subscription Handler. To receive events from server for a subscription
            data_change and event methods are called directly from receiving thread.
            Do not do expensive, slow or network operation there. Create another
            thread if you need to do such a thing
            """
            def datachange_notification(self, node, val, data):
                print("Python: New data change for", node.nodeid, ", ", val)
                me = dict(varID = varID, value = val)
                agent.publish(topic=Topic, payload=json.dumps(me))
            def event_notification(self, event):
                print("Python: New event", event)

        if varID in self.subVarIDList:
            print("There is a subscription to the variable " + varID + " already.")
            self.agent.publish(self.consoleTopic, "There is a subscription to the variable " + varID + " already.")
        else:
            var = self.get_node(varID)
            handler = SubHandler()
            sub = self.create_subscription(period, handler)  # First arguement here is period of checking for data.
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
        print("Before set_node function")
        meth = self.get_node(nodeId)
        print("Method with Browse Name ", str(meth.read_browse_name), "is being called")
        try:
            methodParent: object = meth.get_parent()
            print('\n', methodParent, '\n')
        except:
            print("Could not find the parent of the method with ID: ", nodeId)
            self.agent.publish(str(self.consoleTopic), "Could not find the parent of the method with ID: " + nodeId)
        finally:
            result = methodParent.call_method(meth, *args)
            return result

    def readValue(self, varID):
        var = self.get_node(varID)
        val = var.read_value()
        d = dict(varId = var, value = val)
        ret = json.dumps(d)
        return ret
        # except:
        #     print("Couldn't read the value with ID ", varID)


    def browse_node_tree(self, syncnode):
        """
        Build and return a nested node tree dict by recursion (filtered by OPC UA objects and variables).
        """
        global args
        node_class = syncnode.read_node_class()
        children = []
        def quasarArguementHandling(methnode):
            input_arguments_property = methnode.get_child("InputArguments")
            if input_arguments_property is not None:
                input_arguments = input_arguments_property.get_value()
                arguments = []
                for arg in input_arguments:
                    arguments.append(arg)
                args = str(arguments)
            else:
                args = 'None'
            return args

        for child in syncnode.get_children():
            if child.read_node_class() in [ua.NodeClass.Object, ua.NodeClass.Variable, ua.NodeClass.Method,
                                           ua.NodeClass.ObjectType, ua.Argument]:
                if child.read_node_class() in [ua.NodeClass.Method] and self.type == 'quasar':
                    args = quasarArguementHandling(child)
                else:
                    children.append(
                        self.browse_node_tree(child)
                    )
        if node_class != ua.NodeClass.Variable:
            var_type = node_class
        else:
            try:
                var_type = (syncnode.read_data_type_as_variant_type()).value
            except ua.UaError:
                _logger.warning('Node Variable Type could not be determined for %r', syncnode)
                var_type = 'None'
        if syncnode.read_node_class() in [ua.NodeClass.Method] and self.type == 'quasar':
            return {
                'id': syncnode.nodeid.to_string(),
                'name': (syncnode.read_display_name()).Text,
                'cls': node_class.value,
                'children': children,
                'typeOfNode': str(node_class),
                'arguments': args,
                'type': var_type,
            }
        else:
            return {
                'id': syncnode.nodeid.to_string(),
                'name': (syncnode.read_display_name()).Text,
                'cls': node_class.value,
                'children': children,
                'typeOfNode': str(node_class),
                'type': var_type,
            }

    def browse_server(self):
        """
        Build and return a nested node tree dict by recursion (filtered by OPC UA objects and variables).
        And bring back the architecture of each server.
        """
        return self.browse_node_tree(self.get_root_node())
import sys
import threading
sys.path.insert(0, "..")
import logging
import time
import configparser
import asyncio
from pathlib import Path
import numpy as np
import json
from asyncua import ua, common, sync, Client
from asyncua.sync import DataTypeDictionaryBuilder, syncmethod, SyncNode, ThreadLoop, Client, _logger
from asyncua.sync import syncfunc, Subscription
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, tostring
from dict2xml import dict2xml
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
import paho.mqtt.client as mqtt

import savedSubscriptionConfig

'''

For every server in the industry another client entity should be created to be connected with it                        
url:                    the url of the server that each client will connect to                                          
name:                   the name of each client(same as the server name)                                                
type:                   one of the followings: 'quasar', 'nodeopcua', 'asyncua', 'codesys', 'uanet', 'uasdk', 'open62541'         
mqtturl:                the url/name of the mqtt broker through which the data are transferred to/from the Platform     
mqttport:               the port of the mqtt broker through which the data are transferred to/from the Platform         
architecturetopic:      the mqtt topic in which the nodes of the server will be posted after connecting to it           
consoletopic:           the mqtt topic where console-type messages are posted                                           
readtopic:              the mqtt topic where the read-asked values are published                                        
methRequestTopic:       the mqtt topic where the UI publishes to call an OPC UA method                                  
readRequestTopic:       the mqtt topic where the UI publishes to request to read the value of a variable               
writeRequestTopic:      the mqtt topic where the UI publishes to request to write the value of a variable               
subRequestTopic:        the mqtt topic where the UI publishes to request to monitor the value changes of a variable     
unSubRequestTopic:      the mqtt topic where the UI publishes to request to stop monitoring variable's value changes    
connectDisconnectTopic: the mqtt topic where the UI publishes to request client-server disconnection and reconnection    

'''


class opcuaClient(Client):
    # This class is a child class to the Client Class from asyncua package.
    # When you add the __init__() function, the child class will no longer inherit the parent's __init__() function.
    # Unless you run the super().__init__ function
    def __init__(self, url: str, name: str, type: str, mqtturl: str, mqttport: int, architecturetopic: str,
                 consoletopic: str,
                 readtopic: str, methRequestTopic: str, readRequestTopic: str, writeRequestTopic: str,
                 subRequestTopic: str, unSubRequestTopic: str, subscribeTopic: str, connectDisconnectTopic: str,
                 count: int):
        super().__init__(url)
        self.url = url
        self.name = name
        self.type = type
        self.count = count
        self.brokerURL = mqtturl
        self.brokerPort = mqttport
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

        # Defining a dictionary for using the information stored in SavedSubscriptions.ini
        self.subscriptionsInfo = {}

        # Defining a dictionary as a data structure for the IDs and ending flags of the variables under subscription.
        self.subscriptionDict = {}

        # TO DO!
        # Add fields that have to do with server's security policy.
        # self.set_security(policy = , certificate = , private_key = , private_key_password = , server_certificate = , mode = )
        self.agent: mqtt.Client = self.createMqttAgent()
        self.initial_subscriptions()



    def finish(self):
        for varid in self.subscriptionDict:
            self.subscriptionDict[varid] = False
            savedSubscriptionConfig.delete_subscription(self.count, varid)
        time.sleep(0.05)
        self.subscriptionDict.clear()
        self.agent.loop_stop()
        self.agent.__del__()
        # TO DO!
        # Delete the document with the subscriptions saved

    def make_saved_subscriptions(self):
        try:
            with open('Subscriptions.json', 'r') as subDocument:
                subData = json.load(subDocument)
        except:
            subData = []

        if subData:
            for item in subData:
                if item['servercount'] == self.count:
                    self.subToVarID(varID=item['id'], period=item['period'], Topic=self.subscribeTopic, token=item["assignmentToken"])

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
            if msg.topic == self.methRequestTopic:
                mess = json.loads(msg.payload)
                print("Call of method", mess["methodID"], " was ordered.")
                cons = json.dumps({"message":"Call of method " + mess["methodID"] + " was ordered."})
                agent.publish(str(self.consoleTopic), cons)
                if len(mess) == 1:
                    callMeth = self.callMethodFromNodeID(mess["methodID"])
                elif len(mess) == 2:
                    self.callMethodFromNodeID(mess["methodID"], mess["arg1"])
                elif len(mess) == 3:
                    callMeth = self.callMethodFromNodeID(str(mess["methodID"]), mess["arg1"], mess["arg2"])

            if msg.topic == self.subRequestTopic:
                print("we've got something here")
                mess = json.loads(msg.payload)
                mesg = str(msg.payload.decode("utf-8"))
                print("Subscription on the variable " + mesg + " was ordered.")
                print(str(mess), str(mesg))
                cons = json.dumps({"message":"Subscription on the variable " + mesg + " was ordered."})
                agent.publish(str(self.consoleTopic), cons)

                varID = str(mess["varID"])
                period = mess["SubscriptionPeriod"]
                Topic = self.subscribeTopic
                token = mess["assignmentToken"]

                if varID in self.subscriptionDict:
                    logging.warning("There is a subscription to the variable " + varID + " already.")
                    print("There is a subscription to the variable " + varID + " already.")
                    cons = json.dumps({"message": "There is a subscription to the variable " + varID + " already."})
                    self.agent.publish(self.consoleTopic, cons)
                else:
                    sub_thread = threading.Thread(target=self.subToVarID, args=(varID, period, Topic, token))
                    sub_thread.start()
                    savedSubscriptionConfig.add_subscription(self.count, varID, period, token)


                # self.startSubscription(varID=mess["varID"], period=mess["SubscriptionPeriod"],
                #                        Topic=self.subscribeTopic)

                print('Just after sub call')

            if msg.topic == self.unSubRequestTopic:
                print('Unsubscribe ordered\n')
                unSubObj = json.loads(msg.payload)
                mess = str(msg.payload.decode("utf-8"))
                varid = str(unSubObj['varID'])
                print("the unsubscribe mess is " + mess)

                if varid in self.subscriptionDict:
                    self.unsubFromVarID(varid)
                    savedSubscriptionConfig.delete_subscription(self.count, varid)
                else:
                    print("No subscription found to the variable ", varid, ". The dictionary is:")
                    print(self.subscriptionDict)
                    cons = json.dumps({"message": "No subscription found to the variable " + varid + "."})
                    agent.publish(self.consoleTopic, cons)

                    # cons = json.dumps({"message":"Ending subscription on the variable " + mess + " was ordered."})
                    # agent.publish(self.consoleTopic, cons)

            if msg.topic == self.readRequestTopic:
                mess = str(msg.payload.decode("utf-8"))
                retMess = self.readValue(mess)
                agent.publish(self.readTopic, retMess)
                return retMess

            if msg.topic == self.writeRequestTopic:
                mess = json.loads(msg.payload)
                if len(mess) != 2:
                    cons = json.dumps({"message": "Wrong number of arguements"})
                    agent.publish(self.consoleTopic, cons)
                    print("Wrong number of arguements")
                    return "Wrong number of arguements"
                else:
                    var = self.get_node(mess["varID"])
                    var.set_value(mess["value"])
                    print("var written")

            if msg.topic == self.connectDisconnectTopic:
                mess = str(msg.payload.decode("utf-8"))
                if mess == "disconnect":
                    self.disconnect()
                elif mess == "reconnect":
                    self.connect()

        self.agent = mqtt.Client(self.name)
        self.agent.on_connect = on_connect
        self.agent.on_message = on_message
        self.agent.connect(host=self.brokerURL)
        self.agent.loop_start()

        return self.agent

    def initial_subscriptions(self):
        # From the birth of mqtt agent, we want it to subscribe to the following topics.
        self.agent.subscribe(self.consoleTopic)
        self.agent.subscribe(self.subRequestTopic)
        self.agent.subscribe(self.methRequestTopic)
        self.agent.subscribe(self.unSubRequestTopic)
        self.agent.subscribe(self.readRequestTopic)
        self.agent.subscribe(self.writeRequestTopic)
        self.agent.subscribe(self.connectDisconnectTopic)

        return 0

    def __str__(self):
        return f"{self.name} with url :{self.name} and tloop = {self.tloop}"


    def subToVarID(self, varID, period, Topic, token):
        agent = self.agent
        class SubHandler(object):
            """
            Subscription Handler. To receive events from server for a subscription
            data_change and event methods are called directly from receiving thread.
            Do not do expensive, slow or network operation there. Create another
            """

            def datachange_notification(self, node, val, data):
                print("Python: New data change for" + str(node.nodeid), ", ", str(val) + '\n')
                dt = data.monitored_item.Value.ServerTimestamp
                st = data.monitored_item.Value.SourceTimestamp
                me = dict(varID=varID, value=val, ServerTimestamp=dt.isoformat(), SourceTimestamp=st.isoformat(), assignmentToken = token)
                agent.publish(topic=Topic, payload=json.dumps(me))
                print(val)

            def event_notification(self, event):
                print("Python: New event", event)

        # Creating a new item in the dictionary for this subscription.
        self.subscriptionDict[varID] = True

        with ThreadLoop() as tloop:
            with Client(url=self.url, tloop=tloop) as client:
                print(varID)
                myvar = client.get_node(varID)
                handler = SubHandler()
                sub = client.create_subscription(handler=handler, period=period)
                handle = sub.subscribe_data_change(myvar)
                logging.warning("We're here still alive like a storm you can't stop.")

                while self.subscriptionDict[varID]:
                    time.sleep(0.01)

    def unsubFromVarID(self, varID):
        self.subscriptionDict[varID] = False
        time.sleep(0.3)
        self.subscriptionDict.pop(varID)
        print("Ending subscription on the variable ", varID, " successfully.")


    def callMethodFromNodeID(self, nodeId, *args):
        with ThreadLoop() as tloop:
            with Client(self.url, tloop=tloop) as client:
                meth = client.get_node(nodeId)
                print("Method with Browse Name ", str(meth.read_browse_name), "is being called")
                methodParent = meth.get_parent()
                print("Method with Browse Name ", str(meth.read_browse_name), "is being called")
                res = methodParent.call_method(meth, *args)

    def readValue(self, varID):
        var = self.get_node(varID)
        val = var.read_value()
        d = dict(varId=var, value=val)
        ret = json.dumps(d)
        return ret
        # except:

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
            if child.read_node_class() in [ua.NodeClass.Object, ua.NodeClass.Variable, ua.NodeClass.Method, ua.Argument]:
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

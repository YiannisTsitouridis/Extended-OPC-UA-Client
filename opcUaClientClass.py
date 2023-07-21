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
from paho.mqtt.client import Client as Agent
from paho.mqtt import client
from asyncua.sync import Client, ThreadLoop, _logger

import codecs
import configparser
import sqlalchemy
import collections
import errno
import os
import platform
import select
import socket

import base64
import hashlib
import logging
import string
import struct
import sys
import threading
import time
import uuid

from paho.mqtt.matcher import MQTTMatcher
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCodes
from paho.mqtt.subscribeoptions import SubscribeOptions

"""
This is an MQTT client module. MQTT is a lightweight pub/sub messaging
protocol that is easy to implement and suitable for low powered devices.
"""
import collections
import errno
import os
import platform
import select
import socket

ssl = None
try:
    import ssl
except ImportError:
    pass

socks = None
try:
    import socks
except ImportError:
    pass

try:
    # Python 3
    from urllib import parse as urllib_dot_parse
    from urllib import request as urllib_dot_request
except ImportError:
    # Python 2
    import urllib as urllib_dot_request

    import urlparse as urllib_dot_parse


try:
    # Use monotonic clock if available
    time_func = time.monotonic
except AttributeError:
    time_func = time.time

try:
    import dns.resolver
except ImportError:
    HAVE_DNS = False
else:
    HAVE_DNS = True


if platform.system() == 'Windows':
    EAGAIN = errno.WSAEWOULDBLOCK
else:
    EAGAIN = errno.EAGAIN

# Python 2.7 does not have BlockingIOError.  Fall back to IOError
try:
    BlockingIOError
except NameError:
    BlockingIOError  = IOError

MQTTv31 = 3
MQTTv311 = 4
MQTTv5 = 5

if sys.version_info[0] >= 3:
    # define some alias for python2 compatibility
    unicode = str
    basestring = str

# Message types
CONNECT = 0x10
CONNACK = 0x20
PUBLISH = 0x30
PUBACK = 0x40
PUBREC = 0x50
PUBREL = 0x60
PUBCOMP = 0x70
SUBSCRIBE = 0x80
SUBACK = 0x90
UNSUBSCRIBE = 0xA0
UNSUBACK = 0xB0
PINGREQ = 0xC0
PINGRESP = 0xD0
DISCONNECT = 0xE0
AUTH = 0xF0

# Log levels
MQTT_LOG_INFO = 0x01
MQTT_LOG_NOTICE = 0x02
MQTT_LOG_WARNING = 0x04
MQTT_LOG_ERR = 0x08
MQTT_LOG_DEBUG = 0x10
LOGGING_LEVEL = {
    MQTT_LOG_DEBUG: logging.DEBUG,
    MQTT_LOG_INFO: logging.INFO,
    MQTT_LOG_NOTICE: logging.INFO,  # This has no direct equivalent level
    MQTT_LOG_WARNING: logging.WARNING,
    MQTT_LOG_ERR: logging.ERROR,
}

# CONNACK codes
CONNACK_ACCEPTED = 0
CONNACK_REFUSED_PROTOCOL_VERSION = 1
CONNACK_REFUSED_IDENTIFIER_REJECTED = 2
CONNACK_REFUSED_SERVER_UNAVAILABLE = 3
CONNACK_REFUSED_BAD_USERNAME_PASSWORD = 4
CONNACK_REFUSED_NOT_AUTHORIZED = 5

# Connection state
mqtt_cs_new = 0
mqtt_cs_connected = 1
mqtt_cs_disconnecting = 2
mqtt_cs_connect_async = 3

# Message state
mqtt_ms_invalid = 0
mqtt_ms_publish = 1
mqtt_ms_wait_for_puback = 2
mqtt_ms_wait_for_pubrec = 3
mqtt_ms_resend_pubrel = 4
mqtt_ms_wait_for_pubrel = 5
mqtt_ms_resend_pubcomp = 6
mqtt_ms_wait_for_pubcomp = 7
mqtt_ms_send_pubrec = 8
mqtt_ms_queued = 9

# Error values
MQTT_ERR_AGAIN = -1
MQTT_ERR_SUCCESS = 0
MQTT_ERR_NOMEM = 1
MQTT_ERR_PROTOCOL = 2
MQTT_ERR_INVAL = 3
MQTT_ERR_NO_CONN = 4
MQTT_ERR_CONN_REFUSED = 5
MQTT_ERR_NOT_FOUND = 6
MQTT_ERR_CONN_LOST = 7
MQTT_ERR_TLS = 8
MQTT_ERR_PAYLOAD_SIZE = 9
MQTT_ERR_NOT_SUPPORTED = 10
MQTT_ERR_AUTH = 11
MQTT_ERR_ACL_DENIED = 12
MQTT_ERR_UNKNOWN = 13
MQTT_ERR_ERRNO = 14
MQTT_ERR_QUEUE_SIZE = 15
MQTT_ERR_KEEPALIVE = 16

MQTT_CLIENT = 0
MQTT_BRIDGE = 1

# For MQTT V5, use the clean start flag only on the first successful connect
MQTT_CLEAN_START_FIRST_ONLY = 3


if sys.version_info[0] >= 3:
    # define some alias for python2 compatibility
    unicode = str
    basestring = str

try:
    # Use monotonic clock if available
    time_func = time.monotonic
except AttributeError:
    time_func = time.time

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

class opcuaClient(Client, Agent):
    # This class is a child class to the Client Class from asyncua package.
    # When you add the __init__() function, the child class will no longer inherit the parent's __init__() function.
    # Unless you run the super().__init__ function
    def __init__(self, url: str, name: str, mqtturl: str, mqttport: int, architecturetopic: str, consoletopic: str, readtopic: str, client_id="", clean_session=None, userdata=None,
                 protocol=4, transport="tcp", reconnect_on_failure=True):
        super().__init__(url)
        self.name = name
        self.brokerURL = mqtturl
        self.brokerPort = mqttport
        time.sleep(2)
        self.architectureTopic = architecturetopic
        self.consoleTopic = consoletopic
        self.readTopic = readtopic

        if transport.lower() not in ('websockets', 'tcp'):
            raise ValueError(
                'transport must be "websockets" or "tcp", not %s' % transport)
        self._transport = transport.lower()
        self._protocol = protocol
        self._userdata = userdata
        self._sock = None
        self._sockpairR, self._sockpairW = (None, None,)
        self._keepalive = 60
        self._connect_timeout = 5.0
        self._client_mode = MQTT_CLIENT

        if protocol == client.MQTTv5:
            if clean_session is not None:
                raise ValueError('Clean session is not used for MQTT 5.0')
        else:
            if clean_session is None:
                clean_session = True
            if not clean_session and (client_id == "" or client_id is None):
                raise ValueError(
                    'A client id must be provided if clean session is False.')
            self._clean_session = clean_session

        # [MQTT-3.1.3-4] Client Id must be UTF-8 encoded string.
        if client_id == "" or client_id is None:
            if protocol == MQTTv31:
                self._client_id = base62(uuid.uuid4().int, padding=22)
            else:
                self._client_id = b""
        else:
            self._client_id = client_id
        if isinstance(self._client_id, unicode):
            self._client_id = self._client_id.encode('utf-8')

        self._username = None
        self._password = None
        self._in_packet = {
            "command": 0,
            "have_remaining": 0,
            "remaining_count": [],
            "remaining_mult": 1,
            "remaining_length": 0,
            "packet": bytearray(b""),
            "to_process": 0,
            "pos": 0}
        self._out_packet = collections.deque()
        self._last_msg_in = time_func()
        self._last_msg_out = time_func()
        self._reconnect_min_delay = 1
        self._reconnect_max_delay = 120
        self._reconnect_delay = None
        self._reconnect_on_failure = reconnect_on_failure
        self._ping_t = 0
        self._last_mid = 0
        self._state = mqtt_cs_new
        self._out_messages = collections.OrderedDict()
        self._in_messages = collections.OrderedDict()
        self._max_inflight_messages = 20
        self._inflight_messages = 0
        self._max_queued_messages = 0
        self._connect_properties = None
        self._will_properties = None
        self._will = False
        self._will_topic = b""
        self._will_payload = b""
        self._will_qos = 0
        self._will_retain = False
        self._on_message_filtered = MQTTMatcher()
        self._host = ""
        self._port = 1883
        self._bind_address = ""
        self._bind_port = 0
        self._proxy = {}
        self._in_callback_mutex = threading.Lock()
        self._callback_mutex = threading.RLock()
        self._msgtime_mutex = threading.Lock()
        self._out_message_mutex = threading.RLock()
        self._in_message_mutex = threading.Lock()
        self._reconnect_delay_mutex = threading.Lock()
        self._mid_generate_mutex = threading.Lock()
        self._thread = None
        self._thread_terminate = False
        self._ssl = False
        self._ssl_context = None
        # Only used when SSL context does not have check_hostname attribute
        self._tls_insecure = False
        self._logger = None
        self._registered_write = False
        # No default callbacks
        self._on_log = None
        self._on_connect = None
        self._on_connect_fail = None
        self._on_subscribe = None
        self._on_message = None
        self._on_publish = None
        self._on_unsubscribe = None
        self._on_disconnect = None
        self._on_socket_open = None
        self._on_socket_close = None
        self._on_socket_register_write = None
        self._on_socket_unregister_write = None
        self._websocket_path = "/mqtt"
        self._websocket_extra_headers = None
        # for clean_start == MQTT_CLEAN_START_FIRST_ONLY
        self._mqttv5_first_connect = True
        self.suppress_exceptions = False # For callbacks

        print(self.name)
        print(self.consoleTopic)
        print(self.readTopic, self.brokerURL, self.brokerPort)
        
        self.connectMqttAgent()


    def connectMqttAgent(self):
        def on_connect(agent, userdata, flags, rc):
            if rc == 0:
                print("Agent connected OK")
            else:
                print("Bad agent connection to MQTT Broker with result code " + str(rc))
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.

        def on_message(agent:opcuaClient, userdata, msg):
            print(msg.topic + " " + str(msg.payload))
            logging.basicConfig(level=logging.WARN)
            # logger = logging.getLogger("KeepAlive")
            # logger.setLevel(logging.DEBUG)

            if (msg.topic == str(agent.name) + "/Method_calls"):
                mess = json.loads(msg.payload)
                print("Call of method", mess["methodID"], " was ordered.")
                agent.publish(str(self.consoleTopic), "Call of method " + mess["methodID"] + " was ordered.")
                if len(mess) == 1:
                    callMeth = agent.callMet.callMethodFromNodeID(mess["methodID", self])
                elif len(mess) == 2:
                    callMeth = agent.callMethodFromNodeID(mess["methodID"], self, mess["arg1"])
                    return callMeth
                elif len(mess) == 3:
                    callMeth = agent.callMethodFromNodeID(mess["methodID"], self, mess["arg1"], mess["arg1"])
                    return callMeth

            if (msg.topic == str(agent.name) + "/Subscribe"):
                print("we've got something here")
                mess = json.loads(msg.payload)
                mesg = str(msg.payload.decode("utf-8"))
                print("Subscription on the variable " + mesg + " was ordered.")
                agent.publish(agent.consoleTopic, "Subscription on the variable " + mesg + " was ordered.")
                subvar = agent.subToVarID(mess["varID"], mess["SubscriptionPeriod"])
                return subvar

            if (msg.topic == str(agent.name) + "/Unsubscribe"):
                mess = str(msg.payload.decode("utf-8"))
                unsu = agent.unsubFromVarID(mess)
                print("Ending subscription on the variable ", str(mess), " was ordered.")
                agent.publish(agent.consoleTopic, "Ending subscription on the variable " + str(mess) + " was ordered.")

            if (msg.topic == str(agent.name) + "/Read"):
                mess = msg.payload
                value = agent.readValue(mess)
                agent.publish(agent.readTopic, value)
                return value

            if (msg.payload == str(agent.name) + "/Write"):
                mess = json.loads(msg.payload)
                if len(mess) != 2:
                    agent.publish(agent.consoleTopic, "Wrong number of arguements")
                    return "Wrong number of arguements"
                else:
                    var = agent.get_node(mess["varID"])
                    var.set_value(mess["value"])

        print("Here?")
        self.on_connect = on_connect
        print("or here?")
        self.on_message = on_message
        self.connect_async(self.brokerURL)
        self.loop_start()
        time.sleep(2)

        # host = self.brokerURL
            
    
    def initial_subscriptions(self):
        # From the birth of mqtt agent, we want it to subscribe to the following topics.
        self.subscribe(self.consoleTopic)
        self.subscribe(self.readTopic)
        self.subscribe(str(self.name) + "/Subscribe")
        self.subscribe(str(self.name) + "/Method_calls")
        self.subscribe(str(self.name) + "/Unsubscribe")
        self.subscribe("hotel")
        return 

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

    class SubHandler(object):
        """
        Subscription Handler. To receive events from server for a subscription
        data_change and event methods are called directly from receiving thread.
        Do not do expensive, slow or network operation there. Create another
        thread if you need to do such a thing
        """

        def datachange_notification(self, node, val):
            print("Python: New data change event", node, val)

            # opcuaClient.handlerPost(node, val)

        def event_notification(self, event):
            print("Python: New event", event)

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


    def subToVarID(self, varID, freq):
        agent = self
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
            self.publish(self.consoleTopic, "Subscription on the variable " + varID + "successful.")
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

    # def handlerPost(self, node, val):
    #     self.agent.publish(node, val)


def main():
    def on_connect(self, userdata, flags, rc):
        if rc == 0:
            print("Agent connected OK")
        else:
            print("Bad agent connection to MQTT Broker with result code " + str(rc))
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
                    client.publish("Topic", "Error occurred while trying to connect to server" + str(
                        client.name) + " with url: " + str(client.url))
                resul = client.initial_subscriptions()
                tree = client.browse_server()
                treejs = json.dumps(tree)
                client.publish("arch", treejs)
                print(client.name, " architecture posted:" + "\n \n", tree)
                print("hello!")
                client.loop_start()
                client.subscribe("hotel")
                embed()
            print("reach here")
    print("Reach here!!!!!!")
if __name__ == "__main__":
    main()

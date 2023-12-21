# Extended OPC UA Gateway

## Overview

This software is written under the I4byDesign Competence Center workflow(https://i4bydesign.gr/) to accomplish the operation of a multi-endpoint python-based industrial device operating as a connector between OPC UA servers located on the industrial site and the center’s IOT Platform. However, it has Platform-independent orientation, while third party use is encouraged in prospects of OPC UA spreading and industrial IOT unification.

## Project Details

It is composed of a main program, called general manager, which is actually an MQTT client, waiting to receive commands from the user through its various topics. It manages the number and details of the registered OPC UA servers. The user can add, delete, and edit registered OPC UA servers. Furthermore, the starting function of each OPC UA client instance is included, using the opcUaClientClass which is a class of an asyncua-based OPC UA client with extra features.

The script opcUaClientClass.py implements an OPC UA client with an mqtt broker as a child object, managing the user’s messages coming through MQTT protocol. Every opcUaClientClass instance has their own topics for receiving orders, as f.e. method call, subscription to variable, un-subscribe from variable, read, write and node browsing, defined by the time of their creation. In addition, they have attributed topics for sending data to the user platform or database, f.e. the values from the subscribed variables, the server’s node architecture, console messages and so on.

The system is developed as an attempt to provide an innovative and adaptable solution for industrial environments where a single complex IOT system is needed for a variety of devices. System is designed with some fundamental local memory, storing all asked subscription in a static Json file and all registered OPC UA servers in an .ini file respectively.

## Third-Party Libraries

1. **Paho MQTT**
   - Description: Eclipse Paho MQTT Python client library.
   - License: Eclipse Public License 2.0
   - [Link to Paho MQTT Repository](https://github.com/eclipse/paho.mqtt.python/blob/master/LICENSE.txt)

2. **Asyncua**
   - Description: An asyncio library for OPC UA (Open Platform Communications Unified Architecture) protocol.
   - License: MIT License
   - [Link to Asyncua Repository](https://github.com/FreeOpcUa/opcua-asyncio/blob/master/COPYING)

3. **Python Standard Library**
   - Description: This project makes use of various modules from the Python Standard Library, including but not limited to:
     - `json`: JSON encoding and decoding.
     - `configparser`: Configuration file parsing.
     - `sys`: System-specific parameters and functions.
     - `threading`: Threading support for concurrent execution.
     - `time`: Time-related functions.

   - License: See Python Software Foundation License
   - [Link to Python Software Foundation License] (https://docs.python.org/3/license.html)


## Installation

...

## Usage

...

## Acknowledgments

...

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


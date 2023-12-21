# Extended OPC UA Gateway

## Overview

This software has been developed within the framework of the I4byDesign Competence Center workflow (https://i4bydesign.gr/) with the goal of enabling the operation of a multi-endpoint Python-based industrial device. This device serves as a connector between OPC UA servers located on the industrial site and the center’s IoT platform. Notably, the software is designed with a platform-independent orientation. Furthermore, third-party utilization is encouraged, fostering the broader adoption of OPC UA and contributing to the unification of industrial IoT practices.

## Project Details

The project consists of a main program, known as the "general manager," which operates as an MQTT client. It awaits commands from users through various topics, managing the registration details of OPC UA servers. Users have the capability to add, delete, and edit registered OPC UA servers. Additionally, the general manager includes the starting function for each OPC UA client instance, utilizing the `opcUaClientClass`. This class is based on the `asyncua` library and offers extra features.

The script `opcUaClientClass.py` implements an OPC UA client with an MQTT broker as a child object. It handles user messages received through the MQTT protocol. Each instance of `opcUaClientClass` has its own topics for receiving orders, such as method calls, variable subscriptions, un-subscriptions from variables, reads, writes, and node browsing. These topics are defined at the time of their creation. Furthermore, each instance has attributed topics for sending data to the user platform or database, including values from subscribed variables, the server's node architecture, console messages, and more.

The system aims to provide an innovative and adaptable solution for industrial environments where a single, complex IoT system is required for a variety of devices. The system is designed with fundamental local memory, storing all requested subscriptions in a static JSON file and all registered OPC UA servers in an `.ini` file, respectively.

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


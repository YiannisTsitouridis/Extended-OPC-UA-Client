import runpy
import sys
import os
import time
import paho.mqtt.client as mqtt
import startUp
import threading
from startUp import stop


def main():
    kill = False
    runThread = threading.Thread(target=startUp.main)
    def on_connect(agent, userdata, flags, rc):
        print("Connected!")

    def on_message(agent, userdata, msg):
        print("Recieved something!")
        print(msg.payload)
        mess = str(msg.payload.decode("utf-8"))
        if mess == "stop":
            print("stop ordered")
            # startUp.stop()
            runThread.start()
        elif mess == "startUp":
            print("startUp ordered")
            startUp.main()

    generalAgent = mqtt.Client("general")
    generalAgent.on_connect = on_connect
    generalAgent.on_message = on_message
    generalAgent.connect(host="localhost", port=1883)
    generalAgent.subscribe("generalTopic")
    generalAgent.loop_forever()

if __name__ == "__main__":
    main()


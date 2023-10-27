import sys
import clientConfig
import generalManager

def addServerFromConsole():
    count = clientConfig.addserver()
    generalManager.createClientThread(count)

def editServerFromConsole(i):
    clientConfig.edit_server(i)

#!/usr/bin/python3
import sys
import time
import configparser
import generalManager

def editData():
    file = configparser.ConfigParser()
    file.read("startingData.ini")
    file.remove_section("BasicInfo")
    main()
def main():
    file = configparser.ConfigParser()
    file.read("startingData.ini")

    if file.has_section("BasicInfo"):
        generalManager.main()
    else:
        file.add_section("BasicInfo")
        file.set("BasicInfo","host", input('Mqtt url: '))
        file.set("BasicInfo", "port", input('Mqtt port: '))
        with open(r"startingData.ini", 'w') as configfile:
            file.write(configfile)
        generalManager.main()

if __name__ == "__main__":
    main()
elif __name__ == editData.__name__:
    editData()
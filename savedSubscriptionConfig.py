import configparser
import json

def create_subscriptions_section(num):

    subDocument = configparser.ConfigParser()
    subDocument.read("savedSubscriptions.ini")
    subDocument.add_section("Server"+str(num))
    with open(r"savedSubscriptions.ini", 'w') as configfile:
        subDocument.write(configfile)


def remove_subscriptions_section(num):
    subDocument = configparser.ConfigParser()
    subDocument.read("savedSubscriptions.ini")
    subDocument.remove_section("Server"+str(num))
    with open(r"savedSubscriptions.ini", 'w') as configfile:
        subDocument.write(configfile)

def add_subscription(num, varID, period):
    with open('Subscriptions.json', 'r') as subDocument:
        subData = json.load(subDocument)
    newSubscription = {"servercount": num, "id": varID, "period": period}
    subData.append(newSubscription)

    with open('Subscriptions.json','w') as subDocument:
        json.dump(subData, subDocument, indent=2)


def delete_subscription(num, varID):
    with open('Subscriptions.json', 'r') as subDocument:
        subData = json.load(subDocument)

    index = next((index for index, obj in enumerate(subData) if obj.get("servercount") == num), None)
    subData.pop(index)
    print("Item popped out!")

    with open('Subscriptions.json', 'w'):
        json.dump(subData, subDocument, indent=2)
import json

def add_subscription(num, varID, period, token):
    try:
        with open('Subscriptions.json', 'r') as subDocument:
            subData = json.load(subDocument)
    except FileNotFoundError:
        # If the file doesn't exist, initialize an empty list
        subData = []

    newSubscription = {"servercount": num, "id": varID, "period": period, "assignmentToken": token}
    subData.append(newSubscription)

    with open('Subscriptions.json', 'w') as subDocument:
        json.dump(subData, subDocument, indent=2)

def delete_subscription(num, varID):
    try:
        with open('Subscriptions.json', 'r') as subDocument:
            subData = json.load(subDocument)
    except FileNotFoundError:
        # If the file doesn't exist, nothing to delete
        return
    index = next((index for index, obj in enumerate(subData) if obj.get("id") == varID), None)
    if index is not None:
        subData.pop(index)
        print("Item popped out!")

        with open('Subscriptions.json', 'w') as subDocument:
            json.dump(subData, subDocument, indent=2)

def remove_all_server_subscriptions(num):
    try:
        with open('Subscriptions.json', 'r') as subDocument:
            subData = json.load(subDocument)
    except FileNotFoundError:
        # If the file doesn't exist, initialize an empty list
        subData = []
    if subData:
        for item in subData:
            if item["servercount"] == num:
                subData.remove(item)
        with open('Subscriptions.json', 'w') as subDocument:
            json.dump(subData, subDocument, indent=2)
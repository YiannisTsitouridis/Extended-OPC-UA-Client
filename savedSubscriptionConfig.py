import configparser

def create_subscriptions_section(num):
    subDocument = configparser.ConfigParser()
    subDocument.read("savedSubsriptions.ini")
    subDocument.add_section("Server"+str(num))
    with open(r"savedSubsriptions", 'w') as configfile:
        subDocument.write(configfile)


def remove_subscriptions_section(num):
    subDocument = configparser.ConfigParser()
    subDocument.read("savedSubsriptions.ini")
    subDocument.remove_section("Server"+str(num))
    with open(r"savedSubsriptions", 'w') as configfile:
        subDocument.write(configfile)

def add_subscription(num, varID, period):
    subDocument = configparser.ConfigParser()
    subDocument.read("savedSubsriptions.ini")
    subDocument.set("Server"+str(num), varID, period)

    with open(r"savedSubsriptions", 'w') as configfile:
        subDocument.write(configfile)

def delete_subscription(num, varID):
    subDocument = configparser.ConfigParser()
    subDocument.read("savedSubsriptions.ini")
    subDocument.remove_option("Server" + str(num), varID)

    with open(r"savedSubsriptions", 'w') as configfile:
        subDocument.write(configfile)
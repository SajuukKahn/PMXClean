import time

def __settings__():
    pass

def onconnect():
    SendPacket("R")
    time.sleep(1.5)
    SendPacket("R")
    response = ReceiveResponse()
    if response is None:
        throw

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
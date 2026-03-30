def __settings__():
    pass

def onconnect():
    if SendAndReceive(BuildModbusPacket(3, 4357, 1), False) is None:
        raise

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
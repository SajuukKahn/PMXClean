def __settings__():
    Settings.Footer = new.string("\r\n")

def onconnect():
    SendPacket("20" + "050026:" + Settings.Footer.Value)
    response = ReceiveResponse()
    if response is None or response == "null":
        raise

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
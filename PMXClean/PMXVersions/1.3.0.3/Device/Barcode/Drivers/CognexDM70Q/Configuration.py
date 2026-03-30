def __settings__():
    Settings.Header = new.string("\x02")
    Settings.Footer = new.string("\x03")
    Settings.Delimiter = new.string(",")

def onconnect():
    SendPacket("SET COM.DMCC-RESPONSE 0")
    if SendAndReceive("GET COM.DMCC-RESPONSE", False) is None:
        raise

def ondisconnect():
    SendPacket("TRIGGER OFF")

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
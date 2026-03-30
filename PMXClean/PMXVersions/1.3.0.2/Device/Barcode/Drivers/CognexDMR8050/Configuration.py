def __settings__():
    Settings.Header = new.string("\x02")
    Settings.Footer = new.string("\x03")
    Settings.Delimiter = new.string(",")
    Settings.NoRead = new.string("NOREAD")

def onconnect():
    if SendAndReceive("GET COM.DMCC-RESPONSE", False) is None:
        raise
    SendAndReceive("SET COM.DMCC-RESPONSE 1", False) # Need responses turned on
    SendAndReceive("SET TRIGGER.TYPE 2", False) # Set manual trigger type
    SendAndReceive("SET RESULT.NO-READ-STRING \"" + Settings.NoRead.Value + "\"", False)

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
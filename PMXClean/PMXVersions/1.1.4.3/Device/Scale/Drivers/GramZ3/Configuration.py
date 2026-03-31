def __settings__():
    Settings.Footer = new.string("")

def onconnect():
    response = SendAndReceive("$" + Settings.Footer.Value, False)
    if response is None or not ValidReading(response):
        throw

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
def __settings__():
    Settings.Footer = new.string("\r\n")

def onconnect():
    if SendAndReceive("OUTPUT RS422" + Settings.Footer.Value, False) is None:
        raise

    sendcommand("TRIGGER SOFTWARE")
    sendcommand("TRIGGERCOUNT 1")

def ondisconnect():
    pass

def sendcommand(command):
    response = SendAndReceive(command + Settings.Footer.Value, False)

    if response is None:
        __throwexception__(Exceptions.BadResponse)

def __exceptions__():
    Exceptions.BadResponse = new.exception("#Connection.Exceptions.BadResponseTitle", "#Connection.Exceptions.BadResponse", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
def __settings__():
    pass

def onconnect():
    # Galil specific settings with no class property
    #  AQ (Analog Input Configuration) -> 1 = -5V to +5V, 2 = -10V to +10V, 3 = 0V to +5V, 4 = 0V to +10V
    aq = [3, 3, 3, 3, 3, 3, 3, 3]
    
    response = SendAndReceive("", False)
    if response is None or (not ":" in response and not "?" in response):
        raise

    sendcommand("CO5")
    for i in range(len(aq)):
        sendcommand("AQ" + str(i + 1) + "," + str(aq[i]))

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

    if "?" in response:
        __throwexception__(Exceptions.CommandError, GetGalilError())
        raise

    if not ":" in response:
        __throwexception__(Exceptions.NotGalil, "GalilDMC4xx0")
        raise

    return response

def ondisconnect():
    pass

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.NotGalil = new.exception("#Connection.Exceptions.InvalidDeviceTitle", "#Connection.Exceptions.InvalidDevice", new.enum("Severity", "Error").Value, None)
    Exceptions.CommandError = new.exception("#Controller.Exceptions.CommandErrorTitle", "#Controller.Exceptions.CommandError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
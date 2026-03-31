#DisplayName = Read
#Description = Get a single raw reading from the laser
#Icon = BookOpenMaterialIcon
#Flags = IsPolling

thrown = False

def __inputs__():
    pass

def __run__():
    try:
        response = sendCommand()
        if (response is not None):
            Outputs.Reading.Value = float(ParseReading(response))
            SetSurfaceReading(Outputs.Reading.Value, True)
        else:
            Outputs.Reading.Value = -1.0
            SetSurfaceReading(Outputs.Reading.Value, False)
    except:
        Outputs.Reading.Value = -1.0
        SetSurfaceReading(Outputs.Reading.Value, False)

def __virtual__():
    pass

def sendCommand():
    global thrown
    response = SendAndReceiveBytes("TRIGGERSW" + Settings.Footer.Value, 7, True)
    if response is None:
        if not thrown:
            thrown = True
            __throwexception__(Exceptions.BadResponse)
        raise
    thrown = False
    return response

def __outputs__():
    #Property = True
    #Description = The raw reading from the laser
    Outputs.Reading = new.double(0, 50.0, 150.0, 0.001, 1.0, "mm")

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
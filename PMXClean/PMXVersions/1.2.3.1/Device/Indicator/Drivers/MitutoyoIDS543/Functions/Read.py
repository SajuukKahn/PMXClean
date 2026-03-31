#DisplayName = Read
#Description = Get a reading from the indicator
#Icon = BookOpenMaterialIcon
#SubIcon = IndicatorCustomIcon
#Flags = IsPolling

thrown = False
timeStamp = None

def __inputs__():
    pass

def __run__():
    global timeStamp
    pollRate = GetPollRate()

    if timeStamp is None:
        timeStamp = PVA.System.GetCurrentTime().Value

    while PVA.System.GetCurrentTime().Value < (pollRate + timeStamp):
        PVA.System.Wait(10)

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

    timeStamp = PVA.System.GetCurrentTime().Value

def __virtual__():
    pass

def sendCommand():
    global thrown
    response = SendAndReceive("R", False)
    if response is None:
        if not thrown:
            thrown = True
            __throwexception__(Exceptions.BadResponse)
        raise
    thrown = False
    return response

def __outputs__():
    #Property = true
    #Description = The reading from the indicator
    Outputs.Reading = new.double(0.0, 0.0, 12.7, 0.01, 1.0, "mm")

def __exceptions__():
    Exceptions.BadResponse = new.exception("#Connection.Exceptions.BadResponseTitle", "#Connection.Exceptions.BadResponse", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global timeStamp
    timeStamp = None

def __exceptionrecovery__():
    pass
# DisplayName = Read
# Description = Grab a single reading from the scale
# Icon = BookOpenMaterialIcon
# Flags = IsPolling

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    SendPacket("20" + "050027:" + Settings.Footer.Value)
    response = ReceiveResponse()
    if response is None or response == "null":
        if thrown:
            return
        thrown = True
        __throwexception__(Exceptions.BadResponse)
        return

    thrown = False
    Outputs.Reading.Value = ParseReading(response)
    Outputs.Reading.Units = ParseUnits(response)

def __virtual__():
    pass

def __outputs__():
    #Property = true
    #Description = The reading from the scale
    Outputs.Reading = new.double(0, -1000000, 1000000, 0.1, 1.0, "")

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
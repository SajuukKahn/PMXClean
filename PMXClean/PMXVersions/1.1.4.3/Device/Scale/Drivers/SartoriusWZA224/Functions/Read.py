# DisplayName = Read
# Description = Grab a single reading from the scale
# Icon = BookOpenMaterialIcon
# Flags = IsPolling

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    SendPacket("P" + Settings.Footer.Value)
    response = ReceiveResponse()

    if response is None or response == "null":
        if thrown:
            return
        thrown = True
        __throwexception__(Exceptions.BadResponse, "")
        return

    thrown = False
    Outputs.Reading.Value = ParseReading(response)
    if Outputs.Reading.Value == -99.0:
        if thrown:
            return
        thrown = True
        __throwexception__(Exceptions.ErrorResponse, ParseErrorCode(response))
        return
    
    Outputs.Reading.Units = ParseUnits(response)

def __virtual__():
    pass

def __outputs__():
    #Property = true
    #Description = The reading from the scale
    Outputs.Reading = new.double(0.0000, -1000000, 1000000, 0.1, 1.0, "[Unit]", __source__)

def __exceptions__():
    Exceptions.BadResponse = new.exception("#Connection.Exceptions.BadResponseTitle", "#Connection.Exceptions.BadResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.ErrorResponse = new.exception("#Connection.Exceptions.BadResponseTitle", "#Scale.Exceptions.ErrorResponse {1}", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
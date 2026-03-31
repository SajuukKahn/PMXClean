# DisplayName = Read
# Description = Get a reading from the indicator
# Icon = BookOpenMaterialIcon
# SubIcon = IndicatorCustomIcon
# Flags = IsPolling

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    response = SendAndReceive("R", False)
    if response is None:
        if thrown:
            return
        thrown = True
        __throwexception__(Exceptions.BadResponse)
        return

    thrown = False
    Outputs.Reading.Value = float(ParseReading(response))

def __virtual__():
    pass

def __outputs__():
    #Property = true
    #Description = The reading from the indicator
    Outputs.Reading = new.double()

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
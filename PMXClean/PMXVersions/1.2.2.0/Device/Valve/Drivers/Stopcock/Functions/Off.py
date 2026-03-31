#DisplayName = Off
#Description = Close the stopcock
#Icon = PowerPlugOffMaterialIcon

def __inputs__():
    pass

def __run__():
    if (Settings.OnOutput is None):
        __throwexception__(Exceptions.OnOutputMissing)
        return

    Settings.OnOutput.Set(False)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OnOutputMissing = new.exception("#Valve.Exceptions.OnOutputMissingTitle", "#Valve.Exceptions.OnOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
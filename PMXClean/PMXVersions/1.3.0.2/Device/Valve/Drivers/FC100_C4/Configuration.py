def __settings__():
    # Reserved = true
    #DisplayName = On Output
    Settings.OnOutput = new.output()

def ready():
    if (Settings.OnOutput is None):
        __throwexception__(Exceptions.OnOutputMissing)
        return

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
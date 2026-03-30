def __settings__():
    #Reserved = true
    #DisplayName = On Output
    Settings.OnOutput= new.output()

    #Reserved = true
    #DisplayName = Atom Air Output
    Settings.AtomAirOutput = new.output()

    #DisplayName = Atom Air On Delay
    Settings.AtomAirOnDelay = new.int(50, 0, 3000, 1, 10, "ms")

    #DisplayName = Atom Air Off Delay
    Settings.AtomAirOffDelay = new.int(50, 0, 3000, 1, 10, "ms")

def ready():
    if (Settings.OnOutput is None):
        __throwexception__(Exceptions.OnOutputMissing)
        return

    if (Settings.AtomAirOutput is None):
        __throwexception__(Exceptions.AtomAirOutputMissing)
        return

def __exceptions__():
    Exceptions.OnOutputMissing = new.exception("#Valve.Exceptions.OnOutputMissingTitle", "#Valve.Exceptions.OnOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.AtomAirOutputMissing = new.exception("#Valve.Exceptions.AtomAirOutputMissingTitle", "#Valve.Exceptions.AtomAirOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
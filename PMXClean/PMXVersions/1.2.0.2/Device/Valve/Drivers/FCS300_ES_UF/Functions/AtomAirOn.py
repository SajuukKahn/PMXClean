#DisplayName = Atom Air On
#Description = Turn the Atom Air on
#Icon = PowerPlugMaterialIcon
#SubIcon = SprayValveCustomIcon

def __inputs__():
    pass

def __run__():
    if (Settings.AtomAirOutput is None):
        _throwexception__(Exceptions.AtomAirOutputMissing)
        return

    Settings.AtomAirOutput.Set(True)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AtomAirOutputMissing = new.exception("#Valve.Exceptions.AtomAirOutputMissingTitle", "#Valve.Exceptions.AtomAirOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
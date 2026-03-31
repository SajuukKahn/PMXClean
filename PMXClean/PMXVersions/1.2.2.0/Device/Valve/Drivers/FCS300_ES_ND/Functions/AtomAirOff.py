#DisplayName = Atom Air Off
#Description = Turn the Atom Air off
#Icon = PowerPlugOffMaterialIcon
#SubIcon = SprayValveCustomIcon

def __inputs__():
    pass

def __run__():
    if (Settings.AtomAirOutput is None):
        __throwexception__(Exceptions.AtomAirOutputMissing)
        return

    Settings.AtomAirOutput.Set(False)

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
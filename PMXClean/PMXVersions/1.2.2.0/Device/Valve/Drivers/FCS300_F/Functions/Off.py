#DisplayName = Off
#Description = Turn the valve off
#Icon = PowerPlugOffMaterialIcon

def __inputs__():
    pass

def __run__():
    if (Settings.OnOutput is None):
        __throwexception__(Exceptions.OnOutputMissing)
        return

    if (Settings.AtomAirOutput is None):
        __throwexception__(Exceptions.AtomAirOutputMissing)
        return

    Settings.OnOutput.Set(False)
    PVA.System.Wait(Settings.AtomAirOffDelay.Value)
    Settings.AtomAirOutput.Set(False)

def __outputs__():
    pass

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
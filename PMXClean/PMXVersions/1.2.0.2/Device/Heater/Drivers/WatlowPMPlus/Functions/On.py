#DisplayName = On
#Description = Turn the heater on
#Icon = PowerPlugMaterialIcon
#Flags = IsQuickAction, IsTriggerStep, IsProcessStep

def __inputs__():
    pass

def __run__():
    if (Settings.HeaterOnOutput is None):
        __throwexception__(Exceptions.HeaterOnOutputMissing)
        return

    Settings.HeaterOnOutput.Set(True)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.HeaterOnOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Heater.Exceptions.HeaterOnOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
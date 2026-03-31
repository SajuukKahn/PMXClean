#DisplayName = Toggle Green
#Description = Toggle the green light on/off
#Icon = LedOffMaterialIcon
#Flags = IsQuickAction

def __inputs__():
    pass

def __run__():
    if (Settings.GreenOutput is None):
        __throwexception__(Exceptions.OutputMissing, "GreenOutput")
        return

    Settings.GreenOutput.Value = not Settings.GreenOutput.Value
    Settings.GreenOutput.Set(bool(Settings.GreenOutput.Value))

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
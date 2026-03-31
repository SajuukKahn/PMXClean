# DisplayName = Turn Off
# Description = Turn all light colors off
# Icon = LedVariantOffMaterialIcon
# Flags = IsQuickAction

def __inputs__():
    pass

def __run__():
    if (Settings.RedOutput is None):
        __throwexception__(Exceptions.OutputMissing, "RedOutput")
        return

    if (Settings.GreenOutput is None):
        __throwexception__(Exceptions.OutputMissing, "GreenOutput")
        return

    if (Settings.BlueOutput is None):
        __throwexception__(Exceptions.OutputMissing, "BlueOutput")
        return

    Settings.RedOutput.Set(False)
    Settings.GreenOutput.Set(False)
    Settings.BlueOutput.Set(False)

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
#DisplayName = On
#Description = Turn the light on
#Icon = LedOnMaterialIcon
#Flags = IsQuickAction, IsTriggerStep, IsInspectionStep

def __inputs__():
    pass

def __run__():
    if (Settings.OnOutput is None):
        __throwexception__(Exceptions.OutputMissing)
        return

    Settings.OnOutput.Set(True)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
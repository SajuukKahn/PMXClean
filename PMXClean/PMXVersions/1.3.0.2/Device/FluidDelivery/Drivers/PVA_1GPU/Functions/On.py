#DisplayName = On
#Description = Turn the 1GPU air on
#Icon = PowerPlugMaterialIcon
#SubIcon = ValveOpenMaterialIcon
#Flags = IsQuickAction

def __inputs__():
    pass

def __run__():
    if Settings.AirOutput is None:
        __throwexception__(Exceptions.AirOutputMissing)
        return

    Settings.AirOutput.Set(True)
    Settings.AirOutput.SetDefaultState(True)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AirOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.AirOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
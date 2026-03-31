#DisplayName = Off
#Description = Turn the material pressure off if not set to always on
#Icon = PowerPlugOffMaterialIcon

def __inputs__():
    pass

def __run__():
    if (Settings.OnOutput is None):
        __throwexception__(Exceptions.OnOutputMissing)
        return

    if not AlwaysOn():
        Settings.OnOutput.Set(False)
        Settings.OnOutput.SetDefaultState(False)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OnOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.OnOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
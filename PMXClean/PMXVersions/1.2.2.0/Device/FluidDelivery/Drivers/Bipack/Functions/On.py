#DisplayName = On
#Description = Turn the dispense air on
#Icon = ValveOpenMaterialIcon
#Flags = IsQuickAction

def __inputs__():
    pass

def __run__():
    if Settings.RefillAirOutput is None:
        __throwexception__(Exceptions.RefillAirOutputMissing)
        return

    if Settings.DispenseAirOutput is None:
        __throwexception__(Exceptions.DispenseAirOutputMissing)
        return

    Settings.RefillAirOutput.Set(False)

    if not AlwaysOff():
        Settings.DispenseAirOutput.Set(True)

        if AlwaysOn():
            Settings.DispenseAirOutput.SetDefaultState(True)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.DispenseAirOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.DispenseAirOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
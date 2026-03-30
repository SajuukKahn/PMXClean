#DisplayName = Check Air Status
#Description = Checks the status of the air input
#Icon = PropaneTankOutlineMaterialIcon
#SubIcon = CheckBoldMaterialIcon
#Flags = IsProcessStep, IsTriggerStep, IsHidden

def __inputs__():
    pass

def __run__():
    if Settings.AirOutput is None:
        __throwexception__(Exceptions.AirOutputMissing)
        return

    if Settings.AirInput is None:
        __throwexception__(Exceptions.AirInputMissing)
        return

    Outputs.AirStatus.Value = (Settings.AirOutput.Value == True) and (Settings.AirInput.Value == True)
    if Outputs.AirStatus.Value == False:
        __throwexception__(Exceptions.AirOffException)

def __virtual__():
    pass

def __outputs__():
    Outputs.AirStatus = new.bool(False, True)

def __exceptions__():
    Exceptions.AirOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.AirOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.AirInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#FluidDelivery.Exceptions.AirInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.AirOffException = new.exception("#FluidDelivery.Exceptions.PVA1GPUExceptionTitle", "#FluidDelivery.Exceptions.AirOffException", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
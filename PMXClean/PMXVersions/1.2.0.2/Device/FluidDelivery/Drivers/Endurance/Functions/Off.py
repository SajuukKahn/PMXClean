#DisplayName = Off
#Description = Clear the cycle start output and wait the complete input
#Icon = PowerPlugOffMaterialIcon

def __inputs__():
    #Description = The time to wait for Cycle Complete before error
    Inputs.Timeout = new.double(5000)

def __run__():
    if (Settings.CycleStart is None):
        __throwexception__(Exceptions.CycleStartMissing)
        return

    if (Settings.CycleComplete is None):
        __throwexception__(Exceptions.CycleCompleteMissing)
        return

    Settings.CycleStart.Set(False)

    complete = Settings.CycleComplete.Value
    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
    while (complete is False) and (PVA.System.GetCurrentTime().Value < timeout):
        if PVA.System.GetCurrentTime().Value > timeout:
            __throwexception__(Exceptions.OffTimeout)
            return

        complete = Settings.CycleComplete.Value
        PVA.System.Wait(10)

    StopMonitoring()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.CycleStartMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.CycleStartMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.CycleCompleteMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#FluidDelivery.Exceptions.CycleCompleteMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OffTimeout = new.exception("#FluidDelivery.Exceptions.EnduranceTitle", "#FluidDelivery.Exceptions.OffTimeout", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
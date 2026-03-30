#DisplayName = On
#Description = Set the cycle start output and wait the complete input
#Icon = PowerPlugMaterialIcon

def __inputs__():
    pass

def __run__():
    if (Settings.CycleStart is None):
        __throwexception__(Exceptions.CycleStartMissing)
        return

    if (Settings.CartReady is None):
        __throwexception__(Exceptions.CartReadyMissing)
        return

    Settings.CycleStart.Set(True)
    StartMonitoring()

    ready = Settings.CartReady.Value
    timeout = PVA.System.GetCurrentTime().Value + Settings.Timeout.Value
    while (ready is False) and (PVA.System.GetCurrentTime().Value < timeout):
        if PVA.System.GetCurrentTime().Value > timeout:
            __throwexception__(Exceptions.OnTimeout)
            return

        ready = Settings.CartReady.Value
        PVA.System.Wait(10)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.CycleStartMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.CycleStartMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.CartReadyMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#FluidDelivery.Exceptions.CartReadyMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OnTimeout = new.exception("#FluidDelivery.Exceptions.EnduranceTitle", "#FluidDelivery.Exceptions.OnTimeout", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
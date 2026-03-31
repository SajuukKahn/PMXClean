def __settings__():
    #DisplayName = Machine Ready
    Settings.MachineReady = new.output()

    #DisplayName = Cycle Start
    Settings.CycleStart = new.output()

    Settings.Refill = new.output()

    #DisplayName = Cart Ready
    Settings.CartReady = new.input()

    #DisplayName = Cycle Complete
    Settings.CycleComplete = new.input()

    #DisplayName = Cart Error
    Settings.CartError = new.input()

    #Description = The time to wait for Cart Ready or Cycle Complete before error
    Settings.Timeout = new.int(5000, 0, 1000000, 10, 100, "ms")

def ready():
    if (Settings.MachineReady is None):
        __throwexception__(Exceptions.MachineReadyMissing)
        return

    if (Settings.CycleStart is None):
        __throwexception__(Exceptions.CycleStartMissing)
        return

    if (Settings.Refill is None):
        __throwexception__(Exceptions.RefillMissing)
        return

    if (Settings.CartReady is None):
        __throwexception__(Exceptions.CartReadyMissing)
        return

    if (Settings.CycleComplete is None):
        __throwexception__(Exceptions.CycleCompleteMissing)
        return

    if (Settings.CartError is None):
        __throwexception__(Exceptions.CartErrorMissing)
        return

    On()

def complete():
    Off()

def __exceptions__():
    Exceptions.MachineReadyMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.MachineReadyMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.CycleStartMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.CycleStartMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.RefillMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.RefillMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.CartReadyMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#FluidDelivery.Exceptions.CartReadyMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.CycleCompleteMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#FluidDelivery.Exceptions.CycleCompleteMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.CartErrorMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#FluidDelivery.Exceptions.CartErrorMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = Down
#Description = Put the actuator in the "down" state and check to ensure it succeeded
#Icon = ArrowDownBoldMaterialIcon
#Flags = IsProcessStep, IsQuickAction

def __inputs__():
    #Description = The maximum amount of time to wait for the actuator to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    if Settings.Output is None:
        __throwexception__(Exceptions.OutputMissing)
        return

    Down()
    DownCheck(Inputs.Timeout)

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
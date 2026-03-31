#DisplayName = Toggle
#Description = Toggle to the opposite of the currently active state
#Icon = BoomGateMaterialIcon
#Flags = IsMappable, IsHidden

def __inputs__():
    #Description = The maximum amount of time to wait for the actuator to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    if Settings.Output is None:
        __throwexception__(Exceptions.OutputMissing)
        return

    if Settings.Output.Value == Settings.ActuatedState.Value:
        Up()
        UpCheck(Inputs.Timeout)
    else:
        Down()
        DownCheck(Inputs.Timeout)

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
#DisplayName = Wait Until On
#Description = Wait for the exhaust to be in the "good" state
#Icon = ClockCheckOutlineMaterialIcon
#Flags = IsHidden

def __inputs__():
    #Description = The maximum amount of time to wait for the exhaust to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    try:
        waitForOn()
    except:
        return

def __virtual__():
    pass

def waitForOn():
    if (Settings.Input is None):
        Outputs.Passed.Value = False
        __throwexception__(Exceptions.InputMissing)
        raise

    onState = Settings.OnState.Value
    result = not onState
    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value

    while result != onState and PVA.System.GetCurrentTime().Value < timeout:
        state = CheckState()
        if state is None:
            break
        result = state
        PVA.System.Wait(10)

    Outputs.OnPassed.Value = result == onState
    if Outputs.Passed.Value == False:
        __throwexception__(Exceptions.Timeout)
        raise

def __outputs__():
    #DisplayName = On Passed
    #Description = A value indicating whether the wait completed successfully or timed out
    Outputs.OnPassed = new.bool(False)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#IO.Exceptions.OnTimeout", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
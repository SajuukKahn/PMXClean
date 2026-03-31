# DisplayName = Wait Until On
# Description = Wait for the sensor to be in the "on" state
# Icon = ClockCheckOutlineMaterialIcon
# Flags = IsHidden

def __inputs__():
    #Description = The maximum amount of time to wait for the sensor to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    if (Settings.Input is None):
        Outputs.Passed.Value = False
        __throwexception__(Exceptions.InputMissing)

    passed = False
    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value

    while passed == False:
        state = _PollState_.PolledState.Value and _PollState_.IsSettled.Value
        if state is None:
            __throwexception__(Exceptions.StateIsNull)
        passed = state
        if PVA.System.GetCurrentTime().Value > timeout:
            break
        PVA.System.Wait(10)

    Outputs.Passed.Value = passed

    if Outputs.Passed.Value == False:
        __throwexception__(Exceptions.Timeout)

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating whether the wait completed successfully or timed out
    Outputs.Passed = new.bool(False)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#IO.Exceptions.OnTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.StateIsNull = new.exception("#Sensor.Exceptions.CheckStateFailedTitle", "#Sensor.Exceptions.CheckStateFailed", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

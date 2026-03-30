#DisplayName = Wait Until X On
#Description = Wait until the X Sensor turns on
#Icon = ClockCheckOutlineMaterialIcon
#Flags = IsHidden

def __inputs__():
    #Description = The maximum amount of time to wait for the sensor to turn on
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    if (Settings.XSensor is None):
        Outputs.Passed.Value = False
        __throwexception__(Exceptions.InputMissing)
        return

    passed = False
    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value

    while passed == False:
        state = CheckXState().State
        if state is None:
            __throwexception__(Exceptions.StateIsNull, "X")
        passed = state.Value
        if PVA.System.GetCurrentTime().Value > timeout:
            break
        PVA.System.Wait(10)

    Outputs.Passed.Value = passed

    if Outputs.Passed.Value == False:
        __throwexception__(Exceptions.Timeout)

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating whether the sensor turned on without timing out
    Outputs.Passed = new.bool(False, True)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#IO.Exceptions.OnTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.StateIsNull = new.exception("#Sensor.Exceptions.CheckStateFailedTitle", "#Sensor.Exceptions.CheckStateFailed", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple(["X Sensor", name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

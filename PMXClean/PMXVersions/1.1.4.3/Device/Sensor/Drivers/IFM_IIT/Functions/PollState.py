# DisplayName = Poll State
# Description = Poll the state of the sensor
# Icon = PollMaterialIcon
# Flags = IsPolling, IsHidden

thrown = False
timeStamp = None
lastState = False

def __inputs__():
    pass

def __run__():
    global thrown
    global timeStamp
    global lastState

    sensorInput = Settings.Input

    if sensorInput is None:
        Outputs.PolledState.Value = False
        Outputs.IsSettled.Value = True
        timeStamp = None
        lastState = False
        if thrown:
            return
        thrown = True
        __throwexception__(Exceptions.InputMissing)
        return
    thrown = False

    currentState = sensorInput.Value == Settings.OnState.Value

    if (lastState != currentState):
        timeStamp = PVA.System.GetCurrentTime().Value
        Outputs.IsSettled.Value = False

    if (timeStamp is not None):
        if PVA.System.GetCurrentTime().Value > (Settings.DebounceTime.Value + timeStamp):
            Outputs.PolledState.Value = currentState
            Outputs.IsSettled.Value = True
            timeStamp = None

    lastState = currentState

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Polled State
    #Description = A value indicating the polled state of the sensor
    Outputs.PolledState = new.bool(False)

    #Property = True
    #Private = True
    #DisplayName = Is Settled
    #Description = A value indicating that the state of the sensor is stable
    Outputs.IsSettled = new.bool(True)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
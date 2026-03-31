# DisplayName = Up Check
# Description = Check if the actuator is in the "up" state
# Icon = ArrowUpBoldMaterialIcon
# SubIcon = CheckMaterialIcon

def __inputs__():
    #Description = The maximum amount of time to wait for the actuator to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    if (Settings.LeftInput is None):
        __throwexception__(Exceptions.InputMissing, "Left Input")
        return
    if (Settings.RightInput is None):
        __throwexception__(Exceptions.InputMissing, "Right Input")
        return
    if (Settings.Output is None):
        __throwexception__(Exceptions.OutputMissing)
        return

    leftup = isleftup()
    rightup = isrightup()
    done = (leftup and rightup) or isactuated()

    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
    while not done and (PVA.System.GetCurrentTime().Value < timeout):
        leftup = isleftup()
        rightup = isrightup()
        done = (leftup and rightup) or isactuated()
        PVA.System.Wait(10)

    Outputs.IsUp.Value = leftup and rightup
    if not done:
        if not leftup:
            __throwexception__(Exceptions.Timeout, "Left Input")
        else:
            __throwexception__(Exceptions.Timeout, "Right Input")
        return

def __virtual__():
    PVA.System.Wait(Inputs.Timeout.Value / 10)

def __outputs__():
    #DisplayName = Is Up
    #Description = A value indicating whether the actuator is in the "up" state
    Outputs.IsUp = new.bool(False)

def __exceptions__():
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#Actuator.Exceptions.NamedUpTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)

def isleftup():
    return not Settings.LeftInput.Value

def isrightup():
    return not Settings.RightInput.Value

def isactuated():
    return Settings.Output.WriteValue == Settings.ActuatedState.Value

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

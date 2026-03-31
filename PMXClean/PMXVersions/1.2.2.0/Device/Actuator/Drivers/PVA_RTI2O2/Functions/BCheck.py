#DisplayName = B Check
#Description = Check if the actuator is in the "Position B" state
#Icon = AlphaBBoxMaterialIcon
#SubIcon = CheckMaterialIcon

def __inputs__():
    #Description = The maximum amount of time to wait for the actuator to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    if (Settings.PositionAInput is None):
        __throwexception__(Exceptions.InputMissing, "Position A Input")
        return
    if (Settings.PositionBInput is None):
        __throwexception__(Exceptions.InputMissing, "Position B Input")
        return
    if (Settings.PositionAOutput is None):
        __throwexception__(Exceptions.OutputMissing, "Position A Output")
        return
    if (Settings.PositionBOutput is None):
        __throwexception__(Exceptions.OutputMissing, "Position B Output")
        return

    ata = isata()
    atb = isatb()
    done = (atb and not ata) or not isactuatedb()

    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
    while not done and (PVA.System.GetCurrentTime().Value < timeout):
        ata = isata()
        atb = isatb()
        done = (atb and not ata) or not isactuatedb()
        PVA.System.Wait(10)

    Outputs.BState.Value = atb and not ata
    if not done:
        if not atb:
            __throwexception__(Exceptions.Timeout, "Position A Input")
        else:
            __throwexception__(Exceptions.Timeout, "Position B Input")
        return

def __virtual__():
    PVA.System.Wait(Inputs.Timeout.Value / 10)

def __outputs__():
    #DisplayName = B State
    #Description = A value indicating whether the actuator is in the "Position B" state
    Outputs.BState = new.bool(False)

def __exceptions__():
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#Actuator.Exceptions.NamedRotateBTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def isata():
    return Settings.PositionAInput.Value

def isatb():
    return Settings.PositionBInput.Value

def isactuatedb():
    return (Settings.PositionAOutput.WriteValue != Settings.ActuatedAState.Value) and (Settings.PositionBOutput.WriteValue == Settings.ActuatedBState.Value)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

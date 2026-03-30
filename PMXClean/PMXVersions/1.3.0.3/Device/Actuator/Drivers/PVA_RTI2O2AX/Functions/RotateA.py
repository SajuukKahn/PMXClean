#DisplayName = Rotate A
#Description = Put the actuator in the "Position A" state
#Icon = AlphaABoxOutlineMaterialIcon
#SubIcon = DispenseValveBoldCustomIcon

def __inputs__():
    pass

def __run__():
    if (Settings.PositionAOutput is None):
        __throwexception__(Exceptions.OutputMissing, "Position A Output")
        return
    if (Settings.PositionBOutput is None):
        __throwexception__(Exceptions.OutputMissing, "Position B Output")
        return

    if Settings.ActuatedAState.Value:
        Settings.PositionAOutput.Set(True)
    else:
        Settings.PositionAOutput.Set(False)

    if Settings.ActuatedBState.Value:
        Settings.PositionBOutput.Set(False)
    else:
        Settings.PositionBOutput.Set(True)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
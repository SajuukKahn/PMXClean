#DisplayName = Lock Check
#Description = Check if the actuator is in the "locked" state
#Icon = LockMaterialIcon
#SubIcon = CheckMaterialIcon

def __inputs__():
    #Description = The maximum amount of time to wait for the actuator to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    if (Settings.ExtendedInput is None):
        __throwexception__(Exceptions.InputMissing, "Extended Input")
        return
    if (Settings.RetractedInput is None):
        __throwexception__(Exceptions.InputMissing, "Retracted Input")
        return
    if (Settings.Output is None):
        __throwexception__(Exceptions.OutputMissing)
        return

    done = isDone() or not isLocked()

    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
    while not done and (PVA.System.GetCurrentTime().Value < timeout):
        done = isDone() or not isLocked()
        PVA.System.Wait(10)

    done = isDone() or not isLocked()
    Outputs.IsLocked.Value = isDone()
    if not Outputs.IsLocked.Value:
        if not lockExtended:
            __throwexception__(Exceptions.Timeout, Settings.ExtendedInput.DisplayName)
        else:
            __throwexception__(Exceptions.Timeout, Settings.RetractedInput.DisplayName)
        return

def __virtual__():
    PVA.System.Wait(Inputs.Timeout.Value / 10)

def __outputs__():
    #DisplayName = Is Locked
    #Description = A value indicating whether the actuator is in the "locked" state
    Outputs.IsLocked = new.bool(False, True)

def __exceptions__():
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#Actuator.Exceptions.NamedLockTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)

def isLockExtended():
    return Settings.ExtendedInput.Value

def isLockRetracted():
    return Settings.RetractedInput.Value

def isDone():
    return isLockExtended() and not isLockRetracted()

def isLocked():
    return Settings.Output.WriteValue == Settings.LockedState.Value

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

#DisplayName = Unlock Check
#Description = Check if the actuator is in the "unlocked" state
#Icon = LockOpenMaterialIcon
#SubIcon = CheckMaterialIcon

def __inputs__():
    #Description = The maximum amount of time to wait for the actuator to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    if (Settings.LockAExtended is None):
        __throwexception__(Exceptions.InputMissing, "Lock A Extended")
        return

    if (Settings.LockBExtended is None):
        __throwexception__(Exceptions.InputMissing, "Lock B Extended")
        return

    if (Settings.LockOutput is None):
        __throwexception__(Exceptions.OutputMissing, "Lock Output")
        return

    if (Settings.UnlockOutput is None):
        __throwexception__(Exceptions.OutputMissing, "Unlock Output")
        return

    done = isDone() or isLocked()

    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
    while not done and (PVA.System.GetCurrentTime().Value < timeout):
        done = isDone() or isLocked()
        PVA.System.Wait(10)

    done = isDone() or isLocked()
    Outputs.IsUnlocked.Value = isDone()
    if not Outputs.IsUnlocked.Value:
        if not isAUnlocked():
            __throwexception__(Exceptions.Timeout, Settings.LockARetracted.DisplayName)
        else:
            __throwexception__(Exceptions.Timeout, Settings.LockBRetracted.DisplayName)
        return

def __virtual__():
    PVA.System.Wait(Inputs.Timeout.Value / 10)

def __outputs__():
    #DisplayName = Is Unlocked
    #Description = A value indicating whether the actuator is in the "unlocked" state
    Outputs.IsUnlocked = new.bool(False, True)

def __exceptions__():
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#Actuator.Exceptions.NamedLockTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def isAUnlocked():
    return Settings.LockARetracted.Value

def isBUnlocked():
    return Settings.LockBRetracted.Value

def isDone():
    return isAUnlocked() and isBUnlocked()

def isLocked():
    return (Settings.LockOutput.WriteValue == Settings.LockedState.Value) and (Settings.UnlockOutput.WriteValue != Settings.LockedState.Value)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

#DisplayName = Unlock Check
#Description = Check if the actuator is in the "unlocked" state
#Icon = LockOpenVariantMaterialIcon
#SubIcon = CheckMaterialIcon

def __inputs__():
    #Description = The maximum amount of time to wait for the actuator to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    if (Settings.Input is None):
        __throwexception__(Exceptions.InputMissing)
        return
    if (Settings.Output is None):
        __throwexception__(Exceptions.OutputMissing)
        return

    unlocked = isunlocked()
    done = unlocked or isactuated()

    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
    while not done and (PVA.System.GetCurrentTime().Value < timeout):
        unlocked = isunlocked()
        done = unlocked or isactuated()
        PVA.System.Wait(10)

    unlocked = isunlocked()
    done = unlocked or isactuated()
    Outputs.IsUnlocked.Value = unlocked
    if not done:
        __throwexception__(Exceptions.Timeout)
        return

def __virtual__():
    #PVA.System.Wait(Inputs.Timeout.Value / 10)
    pass

def __outputs__():
    #DisplayName = Is Unlocked
    #Description = A value indicating whether the actuator is in the "unlocked" state
    Outputs.IsUnlocked = new.bool(False, True)

def __exceptions__():
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#Actuator.Exceptions.UpTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)

def isunlocked():
    return not Settings.Input.Value

def isactuated():
    return Settings.Output.WriteValue == Settings.LockedState.Value

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

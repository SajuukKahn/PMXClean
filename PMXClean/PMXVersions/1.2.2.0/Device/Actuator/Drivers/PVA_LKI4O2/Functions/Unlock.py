#DisplayName = Unlock
#Description = Put the actuator in the "unlocked" state
#Icon = LockOpenOutlineMaterialIcon

def __inputs__():
    pass

def __run__():
    if (Settings.LockOutput is None):
        __throwexception__(Exceptions.OutputMissing, "Lock Output")
        return

    if (Settings.UnlockOutput is None):
        __throwexception__(Exceptions.OutputMissing, "Unlock Output")
        return

    if (Settings.LockedState.Value):
        Settings.LockOutput.Set(False)
        Settings.UnlockOutput.Set(True)
    else:
        Settings.LockOutput.Set(True)
        Settings.UnlockOutput.Set(False)

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
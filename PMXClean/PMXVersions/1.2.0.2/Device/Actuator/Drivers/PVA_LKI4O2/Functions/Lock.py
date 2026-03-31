#DisplayName = Lock
#Description = Put the actuator in the "locked" state
#Icon = LockOutlineMaterialIcon

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
        Settings.UnlockOutput.Set(False)
        Settings.LockOutput.Set(True)
    else:
        Settings.UnlockOutput.Set(True)
        Settings.Output.Set(False)

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
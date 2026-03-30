#DisplayName = Status
#Description = Monitors the status of the Lock
#Icon = PollMaterialIcon
#Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    if (Settings.LockAExtended is not None) and (Settings.LockBExtended is not None):
        Outputs.Locked.Value = Settings.LockAExtended.Value and Settings.LockBExtended.Value

    if (Settings.LockARetracted is not None) and (Settings.LockBRetracted is not None):
        Outputs.Unlocked.Value = Settings.LockARetracted.Value and Settings.LockBRetracted.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Locked
    #Description = A value indicating whether the locks are in the "locked" state
    Outputs.Locked = new.bool(False, True)

    #Property = True
    #DisplayName = Unlocked
    #Description = A value indicating whether the locks are in the "unlocked" state
    Outputs.Unlocked = new.bool(False, True)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

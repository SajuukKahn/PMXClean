#DisplayName = Status
#Description = Monitors the status of the Actuator
#Icon = PollMaterialIcon
#Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    if (Settings.Input is not None):
        Outputs.IsLocked.Value = Settings.Input.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Is Locked
    #Description = A value indicating whether the actuator is in the "locked" state
    Outputs.IsLocked = new.bool(False)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

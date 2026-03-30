#DisplayName = Status
#Description = Monitors the status of the Laser
#Icon = PollMaterialIcon
#Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    if (Settings.OnOutput is not None):
        Outputs.IsOn.Value = Settings.OnOutput.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Is On
    #Description = A value indicating whether the laser is in the "on" state
    Outputs.IsOn = new.bool(False, True)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

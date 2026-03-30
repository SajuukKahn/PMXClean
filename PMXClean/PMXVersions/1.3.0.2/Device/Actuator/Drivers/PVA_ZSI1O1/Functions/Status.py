#DisplayName = Status
#Description = Monitors the status of the Actuator
#Icon = PollMaterialIcon
#Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    if (Settings.Input is not None):
        Outputs.IsDown.Value = Settings.Input.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Is Down
    #Description = A value indicating whether the actuator is in the "down" state
    Outputs.IsDown = new.bool(False, True)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

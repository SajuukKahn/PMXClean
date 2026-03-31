# DisplayName = Status
# Description = Monitors the status of the Locator
# Icon = PollMaterialIcon
# Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    if (Settings.LeftInput is not None and Settings.RightInput is not None):
        Outputs.IsDown.Value = Settings.LeftInput.Value and Settings.RightInput.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Is Down
    #Description = A value indicating whether the actuator is in the "down" state
    Outputs.IsDown = new.bool(False)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

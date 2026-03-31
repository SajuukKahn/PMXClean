#DisplayName = Status
#Description = Monitors the status of the Lights
#Icon = PollMaterialIcon
#Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    if (Settings.RedOutput is not None):
        Outputs.IsRedOn.Value = Settings.RedOutput.Value
    if (Settings.GreenOutput is not None):
        Outputs.IsGreenOn.Value = Settings.GreenOutput.Value
    if (Settings.BlueOutput is not None):
        Outputs.IsBlueOn.Value = Settings.BlueOutput.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Is Red On
    #Description = A value indicating whether the red light is in the "on" state
    Outputs.IsRedOn = new.bool(False)

    #Property = True
    #DisplayName = Is Green On
    #Description = A value indicating whether the green light is in the "on" state
    Outputs.IsGreenOn = new.bool(False)

    #Property = True
    #DisplayName = Is Blue On
    #Description = A value indicating whether the blue light is in the "on" state
    Outputs.IsBlueOn = new.bool(False)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

#DisplayName = Status
#Description = Monitors the status of the Actuator
#Icon = PollMaterialIcon
#Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    if (Settings.PositionAInput is not None):
        Outputs.IsRotatedA.Value = Settings.PositionAInput.Value
    if (Settings.PositionBInput is not None):
        Outputs.IsRotatedB.Value = Settings.PositionBInput.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Is Rotated A
    #Description = A value indicating whether the actuator is in the "Rotated A" state
    Outputs.IsRotatedA = new.bool(False)

    #Property = True
    #DisplayName = Is Rotated B
    #Description = A value indicating whether the actuator is in the "Rotated B" state
    Outputs.IsRotatedB = new.bool(False)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

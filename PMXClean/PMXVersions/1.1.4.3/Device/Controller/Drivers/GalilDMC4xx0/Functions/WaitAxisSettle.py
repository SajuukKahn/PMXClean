# DisplayName = Wait Axis Settle
# Description = Wait for an axis to settle to a maximum amount of error magnitude for a minimum amount of time
# Icon = RayStartEndMaterialIcon
# Flags = IsHidden
# Groups = Motion

def __inputs__():
    #Description = The axis to settle
    Inputs.Axis = new.axis("Controller0")
    
    #Private = True
    #Description = The allowed settling error
    Inputs.Distance = new.int(0, 0, 100, 1, 10, "[Unit]", Inputs.Axis)
    
    #Private = True
    #DisplayName = Settle Time
    #Description = The minimum time to be at the given settle distance
    Inputs.SettleTime = new.double(50, 0, 5000, 1, 10, "ms")

def __run__():
    if Inputs.Axis is not None:
        InternalWaitSettle(Inputs.Axis, Inputs.Distance.Value, Inputs.SettleTime.Value)

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
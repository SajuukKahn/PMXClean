# DisplayName = Stop Axis
# Description = Stop an axis that is in motion
# Icon = RayStartEndMaterialIcon
# Flags = IsHidden
# Groups = Motion

def __inputs__():
    #Description = The axis to stop
    Inputs.Axis = new.axis("Controller0")

    #Description = A value indicating whether the stop should happen with a controlled or abort behavior
    Inputs.Abort = new.bool(False)

def __run__():
    if Inputs.Axis is not None:
        InternalStopAxis(Inputs.Axis, Inputs.Abort)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
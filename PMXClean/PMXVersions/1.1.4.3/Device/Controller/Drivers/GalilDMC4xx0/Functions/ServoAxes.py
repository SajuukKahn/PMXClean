# DisplayName = Servo Axes
# Description = Servo all axes
# Icon = EngineMaterialIcon
# Groups = Motion
# Flags = IsTriggerStep

def __inputs__():
    pass

def __run__():
    axes = GetAxes()
    if len(axes) > 0:
        axesToServo = ""
        for axis in axes:
            if ((axis.LoadState() and (axis.DefaultState is None)) or (axis.DefaultState is True)) and axis.IsActive is True:
                InternalServoAxis(axis)

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
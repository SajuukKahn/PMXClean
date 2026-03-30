#DisplayName = Servo Axes
#Description = Servo all axes
#Icon = EngineMaterialIcon
#Groups = Motion
#Flags = IsTriggerStep

def __inputs__():
    pass

def __run__():
    axes = GetAxes()
    if len(axes) > 0:
        for axis in axes:
            if ((axis.GetLoadState() and (axis.GetDefaultState() is None)) or (axis.GetDefaultState() is True)) and axis.IsActive is True:
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
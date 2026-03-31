# DisplayName = Motor Off
# Description = Turn all motors off
# Icon = EngineOffMaterialIcon
# Groups = Motion
# Flags = IsTriggerStep

def __inputs__():
    pass

def __run__():
    axes = GetAxes()
    if len(axes) > 0:
        for axis in axes:
            InternalStopAxis(axis, True)
            InternalMotorOffAxis(axis)

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
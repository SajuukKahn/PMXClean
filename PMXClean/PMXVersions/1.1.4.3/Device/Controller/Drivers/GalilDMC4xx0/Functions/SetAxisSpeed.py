# DisplayName = Set Axis Speed
# Description = Set the Speed for an axis
# Icon = SpeedometerSlowMaterialIcon
# Flags = IsHidden
# Groups = Motion

def __inputs__():
    #Description = The axis to set speed for
    Inputs.Axis = new.axis("Controller0")

    #Description = The new speed value for the axis
    Inputs.Speed = new.int(20000, 2, 1000000, 10, 100, "[Unit]/s", Inputs.Axis)

def __run__():
    InternalSetAxisSpeed(Inputs.Axis, Inputs.Speed.Value)

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
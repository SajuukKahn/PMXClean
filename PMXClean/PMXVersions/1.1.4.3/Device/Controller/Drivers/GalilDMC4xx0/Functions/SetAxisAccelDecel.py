# DisplayName = Set Axis Accel Decel
# Description = Set the Acceleration and Deceleration parameters for an axis
# Icon = RayStartArrowMaterialIcon
# Flags = IsHidden

def __inputs__():
    #Description = The axis to set accel/decel for
    Inputs.Axis = new.axis("Controller0")
    
    #DisplayName = Acceleration
    #Description = The new acceleration value for the axis
    Inputs.Accel = new.int(300000, 0, 10000000, 1, 10, "[Unit]/s²", Inputs.Axis)
    
    #DisplayName = Deceleration
    #Description = The new deceleration value for the axis
    Inputs.Decel = new.int(300000, 0, 10000000, 1, 10, "[Unit]/s²", Inputs.Axis)

def __run__():
    if Inputs.Axis is not None:
        if not Inputs.Axis.IsLocked.Value and not Inputs.Axis.Status[0].Value:
            SendAndReceive("AC" + Inputs.Axis.ReferenceName + "=" + str(int(Inputs.Accel.Value)), False)
            SendAndReceive("DC" + Inputs.Axis.ReferenceName + "=" + str(int(Inputs.Decel.Value)), False)

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
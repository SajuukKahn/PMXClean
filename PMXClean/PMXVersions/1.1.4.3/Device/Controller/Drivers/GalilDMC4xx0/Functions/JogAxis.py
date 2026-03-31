# DisplayName = Jog Axis
# Description = Jog an axis at a set speed
# Icon = RayStartArrowMaterialIcon
# Groups = Motion

def __inputs__():
    #Description = The axis to jog
    Inputs.Axis = new.axis("Controller0")

    #Description = The speed to jog the axis at
    Inputs.Speed = new.int(5000, -1000000, 1000000, 1, 10, "[Unit]/s", Inputs.Axis)

def __run__():
    if not Inputs.Axis.IsMotionReady:
        PVA.Exceptions.ThrowException(Exceptions.AxisNotReady)
        return

    if Inputs.Axis is not None:
        if not Inputs.Axis.IsLocked.Value and not Inputs.Axis.Status[0].Value:
            Inputs.Axis.Reserve()
            InternalJogAxis(Inputs.Axis, Inputs.Speed)
            Inputs.Axis.Release()

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AxisNotReady = new.exception("#Controller.Exceptions.AxisNotReadyTitle", "#Controller.Exceptions.AxisNotReady", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    InternalStopAxis(Inputs.Axis, True)

def __exceptionrecovery__():
    pass
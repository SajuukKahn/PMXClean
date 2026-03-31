#DisplayName = Move Axis To Position
#Description = Move an axis to a specific point
#Icon = RayStartEndMaterialIcon
#Flags = IsHidden
#Groups = Motion

def __inputs__():
    #Description = The axis to move
    Inputs.Axis = new.axis("Controller0")

    #Description = The position to move to
    Inputs.Position = new.position(0, Inputs.Axis)

def __run__():
    axis = Inputs.Axis

    if axis is None:
        __throwexception__(Exceptions.AxisRequired)
        return

    if not axis.IsMotionReady:
        __throwexception__(Exceptions.AxisNotReady)
        return

    position = Inputs.Position

    if position is None:
        __throwexception__(Exceptions.PositionRequired, "Position")
        return

    waitmotioncomplete(axis)
    setdefaultaxisvalues(axis)

    # Move Axis
    sendcommand("AC" + axis.ReferenceName + "=" + str(int(axis.Acceleration.Value)))
    sendcommand("DC" + axis.ReferenceName + "=" + str(int(axis.Deceleration.Value)))
    sendcommand("PA" + axis.ReferenceName + "=" + str(int(position.Value)))
    sendcommand("BG" + axis.ReferenceName)
    waitmotioncomplete(axis)
    waitsettle(axis)

def __virtual__():
    pass

def setdefaultaxisvalues(*axes):
    for axis in axes:
        if axis is not None:
            sendcommand("AC" + axis.ReferenceName + "=" + str(int(axis.Acceleration.Value)))
            sendcommand("DC" + axis.ReferenceName + "=" + str(int(axis.Deceleration.Value)))
            sendcommand("SP" + axis.ReferenceName + "=" + str(int(axis.Speed.Value)))

def waitmotioncomplete(*axes):
    if axes is not None:
        WaitMotionComplete(axes)

def waitsettle(*axes):
    if axes is not None:
        InternalWaitSettle(axes, 0, 10)

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

def __outputs__():
    pass

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.Axis is not None:
        Inputs.Axis.Reserve()

def __releaseresources__():
    if Inputs.Axis is not None:
        Inputs.Axis.Release()
    PVA.Safety.ResetDoorBypassOK()

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value,  None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisNotReady = new.exception("#Controller.Exceptions.AxisNotReadyTitle", "#Controller.Exceptions.AxisNotReady", new.enum("Severity", "Error").Value, None)
    Exceptions.PositionRequired = new.exception("#Scripting.Exceptions.ScriptValueRequiredTitle", "#Scripting.Exceptions.ScriptValueRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    axis = Inputs.Axis
    if axis is not None:
        StopAxis(axis, True)

def __exceptionrecovery__():
    pass

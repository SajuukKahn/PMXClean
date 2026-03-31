# DisplayName = Move Incremental
# Description = Move a single axis a known distance
# Icon = RayStartArrowMaterialIcon
# Flags = IsMappable
# Groups = Motion

def __inputs__():
    #Description = The axis to move
    Inputs.Axis = new.axis("Controller0")

    #Description = The distance to move by
    Inputs.Distance = new.int(0, -80000, 80000, 10, 100, "[Unit]", Inputs.Axis)

def __run__():
    axis = Inputs.Axis
    distance = int(Inputs.Distance.Value)

    if axis is None:
        __throwexception__(Exceptions.AxisRequired)
        return

    if not axis.IsMotionReady:
        __throwexception__(Exceptions.AxisNotReady)
        return

    if axis is not None:
        axis.IsLocked.Value = True
        sendcommand("ST" + axis.ReferenceName)
        waitmotioncomplete(axis)
        sendcommand("AC" + axis.ReferenceName + "=" + str(int(axis.Acceleration.Value)))
        sendcommand("DC" + axis.ReferenceName + "=" + str(int(axis.Deceleration.Value)))
        sendcommand("SP" + axis.ReferenceName + "=" + str(int(axis.Speed.Value)))
        sendcommand("PR" + axis.ReferenceName + "=" + str(int(distance)))
        sendcommand("BG" + axis.ReferenceName)
        waitmotioncomplete(axis)
        waitsettle(axis)
        axis.IsLocked.Value = False
    else:
        __throwexception__(Exceptions.AxisRequired)

def __virtual__():
    pass

def __outputs__():
    pass

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

def waitmotioncomplete(*axes):
    if axes is not None:
        WaitMotionComplete(axes)

def waitsettle(*axes):
    if axes is not None:
        InternalWaitSettle(axes, 0, 10)

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.Axis is not None:
        Inputs.Axis.Reserve()

def __releaseresources__():
    if Inputs.Axis is not None:
        Inputs.Axis.Release()
    PVA.Safety.ResetDoorBypassOK()

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisNotReady = new.exception("#Controller.Exceptions.AxisNotReadyTitle", "#Controller.Exceptions.AxisNotReady", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    axis = Inputs.Axis
    if axis is not None:
        StopAxis(axis, True)
        axis.IsLocked.Value = False

def __exceptionrecovery__():
    pass
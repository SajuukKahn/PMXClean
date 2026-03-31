# DisplayName = Move To Safe Z
# Description = Move a Robot to the SafeZ coordinate
# Icon = RobotSafeZCustomIcon
# Groups = Motion
# Flags = IsTriggerStep

def __inputs__():
    #Description = The robot to move
    Inputs.Robot = new.robot("Controller0", 0)

def __run__():
    robot = Inputs.Robot
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    z = robot.ZAxis
    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    if not robot.IsMotionReady:
        __throwexception__(Exceptions.RobotNotReady)
        return

    point = robot.SafeZ.Value
    waitmotioncomplete(z)
    setdefaultaxisvalues(z)

    #Move Z
    sendcommand("AC" + z.ReferenceName + "=" + str(int(z.Acceleration.Value)))
    sendcommand("DC" + z.ReferenceName + "=" + str(int(z.Deceleration.Value)))
    sendcommand("PA" + z.ReferenceName + "=" + str(int(point)))
    sendcommand("BG" + z.ReferenceName)
    waitmotioncomplete(z)
    waitsettle(z)

def __virtual__():
    pass

def setdefaultaxisvalues(*axes):
    for axis in axes:
        if axis is not None:
            sendcommand("AC" + axis.ReferenceName + "=" + str(int(axis.Acceleration.Value)))
            sendcommand("DC" + axis.ReferenceName + "=" + str(int(axis.Deceleration.Value)))
            sendcommand("SP" + axis.ReferenceName + "=" + str(int(axis.Speed.Value)))

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)

def waitmotioncomplete(*axes):
    if axes is not None:
        WaitMotionComplete(axes)

def waitsettle(*axes):
    if axes is not None:
        InternalWaitSettle(axes, 0, 10)

def __outputs__():
    pass

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.Robot is not None:
        Inputs.Robot.RequestMove()
        Inputs.Robot.Reserve()

def __releaseresources__():
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
        Inputs.Robot.MoveComplete()
    PVA.Safety.ResetDoorBypassOK()

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotNotReady = new.exception("#Controller.Exceptions.RobotNotReadyTitle", "#Controller.Exceptions.RobotNotReady", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    if Inputs.Robot is not None:
        InternalStopRobot(Inputs.Robot)

def __exceptionrecovery__():
    pass
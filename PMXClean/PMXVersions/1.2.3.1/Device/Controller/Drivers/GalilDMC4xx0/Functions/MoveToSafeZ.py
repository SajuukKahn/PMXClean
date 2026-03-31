#DisplayName = Move To Safe Z
#Description = Move a Robot to the SafeZ coordinate
#Icon = RobotSafeZCustomIcon
#Groups = Motion
#Flags = IsTriggerStep

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

    SetAxisSpeed(z, z.Speed)
    InternalMoveRobotToPosition(robot, new.coordinate(None, None, robot.SafeZ.Value), new.int(0), new.int(10))

def __virtual__():
    robot = Inputs.Robot
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    z = robot.ZAxis
    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    SetAxisSpeed(z, z.Speed)
    InternalMoveRobotToPosition(robot, new.coordinate(None, None, robot.SafeZ.Value), new.int(0), new.int(10))

def waitmotioncomplete(*axes):
    if axes is not None:
        WaitMotionComplete(axes)

def waitsettle(*axes):
    if axes is not None:
        InternalWaitSettle(axes, 0, 10)

def __outputs__():
    pass

def __lockresources__():
    PVA.Safety.SetBypassOK(False)
    if Inputs.Robot is not None:
        Inputs.Robot.RequestMove()
        Inputs.Robot.Reserve()

def __releaseresources__():
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
        Inputs.Robot.MoveComplete()
    PVA.Safety.ResetBypassOK()

def __exceptions__():
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
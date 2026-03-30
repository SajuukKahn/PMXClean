#DisplayName = Move To Safe Z Position
#Description = Move a Robot to a known safe Z position
#Icon = RobotSafeZCustomIcon
#Groups = Motion

def __inputs__():
    #Description = The robot to move
    Inputs.Robot = new.robot("Controller0", 0)
    
    #Description = The safe Z position to move to
    Inputs.SafeZPosition = new.position(0, Inputs.Robot, 2)
    
    #Description = A value indicating whether to only move if the new Z position value is higher
    Inputs.OnlyIfNecessary = new.bool(False)

def __run__():
    robot = Inputs.Robot
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    z = robot.ZAxis
    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    point = min(Inputs.SafeZPosition.Value, robot.SafeZ.Value)

    if not Inputs.OnlyIfNecessary.Value or z.Position.Value < point:
        if not robot.IsMotionReady:
            __throwexception__(Exceptions.RobotNotReady)
            return

        SetAxisSpeed(z, z.Speed)
        InternalMoveRobotToPosition(robot, new.coordinate(None, None, point), new.int(0), new.int(10))

def __virtual__():
    robot = Inputs.Robot
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    z = robot.ZAxis
    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    point = min(Inputs.SafeZPosition.Value, robot.SafeZ.Value)

    if not Inputs.OnlyIfNecessary.Value or z.Position.Value < point:
        SetAxisSpeed(z, z.Speed)
        InternalMoveRobotToPosition(robot, new.coordinate(None, None, robot.SafeZ.Value), new.int(0), new.int(10))

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
#DisplayName = Safe Move To Robot Position
#Description = Move the robot to a position in a safe manner utilizing AllUp and SafeZ
#Icon = ShieldAirplaneMaterialIcon
#Flags = IsHidden
#Groups = Motion

def __inputs__():
    #Description = The robot to move
    Inputs.Robot = new.robot("Controller0", 0)

    #Description = The position to move to
    Inputs.Position = new.coordinate(0, 0, 0, Inputs.Robot)
    
    #DisplayName = Settle Counts
    #Description = The amount of counts to settle to
    Inputs.SettleCounts = new.double(5, 0, 50, 1, 1, "counts")
    
    #DisplayName = Settle Time
    #Description = The minimum time to be at the given settle counts before resuming
    Inputs.SettleTime = new.double(50, 0, 5000, 1, 10, "ms")

def __run__():
    robot = Inputs.Robot
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    if not robot.IsMotionReady:
        __throwexception__(Exceptions.RobotNotReady)
        return

    x = robot.XAxis
    y = robot.YAxis
    z = robot.ZAxis
    theta = robot.ThetaAxis
    point = Inputs.Position

    if x is None:
        __throwexception__(Exceptions.AxisRequired, "X")
        return

    if y is None:
        __throwexception__(Exceptions.AxisRequired, "Y")
        return

    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    InternalSafeMoveRobotToPosition(robot, point, Inputs.SettleCounts.Value, Inputs.SettleTime.Value)

def __virtual__():
    pass

def __virtual__():
    pass

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

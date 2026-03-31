# DisplayName = Line
# Description = Create a line segment command and send it down the motion buffer to run it.
# Icon = VectorLineMaterialIcon
# Flags = IsProgramStep, IsHidden
# Groups = Motion

def __inputs__():
    #Description = The robot to run the vector motion with
    Inputs.Robot = new.robot("Controller0", 0)
    
    #DisplayName = Endpoint
    #Description = The end point of the new line segment
    Inputs.EndPoint = new.coordinate(1000, 0, 0, None, Inputs.Robot)

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

    if x is None:
        __throwexception__(Exceptions.AxisRequired, "X")
        return

    if y is None:
        __throwexception__(Exceptions.AxisRequired, "Y")
        return

    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    point = Inputs.EndPoint
    if (point.X.Value != 0) or (point.Y.Value != 0) or (point.Z.Value != 0) or (point.Theta.IsEnabled and point.Theta.Value != 0):
        if not robot.InUseByProgram:
            robot.ResetVectorMotion()

        robot.InitializeVectorMotion(True)
        AppendVectorLineSegment(robot, point)

        if not robot.InUseByProgram:
            BeginVectorMotion()
            robot.WaitVectorMotionComplete()

def __virtual__():
    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    point = Inputs.EndPoint
    if (point.X.Value != 0) or (point.Y.Value != 0) or (point.Z.Value != 0) or (point.Theta.IsEnabled and point.Theta.Value != 0):
        if not robot.InUseByProgram:
            robot.ResetVectorMotion()

        robot.InitializeVectorMotion(True)
        AppendVectorLineSegment(robot, point)

        if not robot.InUseByProgram:
            BeginVectorMotion()
            robot.WaitVectorMotionComplete()

def __outputs__():
    pass

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
    SendAndReceive("CAS;CSS", False)

def __exceptionrecovery__():
    pass
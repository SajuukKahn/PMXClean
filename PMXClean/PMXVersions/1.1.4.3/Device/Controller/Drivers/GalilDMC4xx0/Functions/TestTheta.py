# DisplayName = Test Theta
# Description = Test the theta calibration by spinning the selected tool in place
# Icon = OrbitMaterialIcon
# Flags = IsHidden

def __inputs__():
    #Description = The robot used to move XY & Theta
    Inputs.Robot = new.robot("Controller0", 0)

    #Description = The tool to spin in place
    Inputs.Tool = new.tool(0)

    #Description = The vector speed to use for coordinated motion
    Inputs.Speed = new.int(20000, 0, 100000, 10, 100, "[Unit]/s", Inputs.Robot, 3)
    
    #DisplayName = Acceleration
    #Description = The vector acceleration to use for coordinated motion
    Inputs.Accel = new.int(200000, 0, 1000000, 10, 100, "[Unit]/s²", Inputs.Robot, 3)
    
    #DisplayName = Deceleration
    #Description = The vector deceleration to use for coordinated motion
    Inputs.Decel = new.int(200000, 0, 1000000, 10, 100, "[Unit]/s²", Inputs.Robot, 3)

def __run__():
    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    if not robot.IsMotionReady:
        __throwexception__(Exceptions.RobotNotReady)
        return

    tool = Inputs.Tool
    x = robot.XAxis
    y = robot.YAxis
    z = robot.ZAxis
    theta = robot.ThetaAxis

    if tool is None:
        __throwexception__(Exceptions.ToolRequired)
        return

    if x is None:
        __throwexception__(Exceptions.AxisRequired, "X")
        return

    if y is None:
        __throwexception__(Exceptions.AxisRequired, "Y")
        return

    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    if theta is None:
        __throwexception__(Exceptions.AxisRequired, "Theta")
        return

    curr = robot.ThetaAxis.Position
    bl = min(robot.ThetaAxis.ReverseLimit.Value + 200, curr)
    fl = max(robot.ThetaAxis.ForwardLimit.Value - 200, curr)

    RotateTheta(robot, tool, new.position(bl), Inputs.Speed, Inputs.Accel, Inputs.Decel)
    RotateTheta(robot, tool, new.position(fl), Inputs.Speed, Inputs.Accel, Inputs.Decel)
    RotateTheta(robot, tool, new.position(curr), Inputs.Speed, Inputs.Accel, Inputs.Decel)

def __virtual__():
    pass

def __outputs__():
    pass

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.Robot is not None:
        Inputs.Robot.Reserve()

def __releaseresources__():
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
    PVA.Safety.ResetDoorBypassOK()

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotNotReady = new.exception("#Controller.Exceptions.RobotNotReadyTitle", "#Controller.Exceptions.RobotNotReady", new.enum("Severity", "Error").Value, None)
    Exceptions.ToolRequired = new.exception("#Tool.Exceptions.NoToolTitle", "#Tool.Exceptions.NoTool", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
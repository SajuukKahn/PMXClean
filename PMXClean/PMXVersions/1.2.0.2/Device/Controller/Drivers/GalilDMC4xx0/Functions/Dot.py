#DisplayName = Dot
#Description = Turn a dispense tool on for a specified amount of time in the current location using RTOS
#Icon = RadioboxMarkedMaterialIcon
#Flags = IsProgramStep, IsHidden
#Groups = Motion

def __inputs__():
    #Description = The robot to dispense the dot with
    Inputs.Robot = new.robot("Controller0", 0)
    
    #DisplayName = On Dwell
    #Description = The amount of time to wait after turning the tool on
    Inputs.OnDwell = new.int(100, 0, 1000000, 10, 100, "ms")
    
    #DisplayName = Off Dwell
    #Description = The amount of time to wait after turning the tool off
    Inputs.OffDwell = new.int(100, 0, 1000000, 10, 100, "ms")
    
    #DisplayName = Retract Distance
    #Description = The distance to retract after the dot has been dispensed
    Inputs.RetractDistance = new.position(0, Inputs.Robot, 2)

def __run__():
    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    if not robot.IsMotionReady:
        __throwexception__(Exceptions.RobotNotReady)
        return

    z = robot.ZAxis

    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    if robot.InUseByProgram:
        sendcommand("dwell_on=" + str(int(Inputs.OnDwell.Value)))
        sendcommand("dwell_of=" + str(int(Inputs.OffDwell.Value)))
        ExecuteRoutine("#dot", new.int(1), new.bool(True))

    if Inputs.RetractDistance.Value != 0:
        robot.InitializeVectorMotion(False)
        AppendVectorLineSegment(robot, new.coordinate(0, 0, Inputs.RetractDistance.Value))
        BeginVectorMotion()
        robot.WaitVectorMotionComplete()

def __virtual__():
    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    PVA.System.Wait(Inputs.OnDwell.Value + Inputs.OffDwell.Value)

    if Inputs.RetractDistance.Value != 0:
        robot.InitializeVectorMotion(False)
        AppendVectorLineSegment(robot, new.coordinate(0, 0, Inputs.RetractDistance.Value))
        BeginVectorMotion()
        robot.WaitVectorMotionComplete()

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

def __outputs__():
    pass

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
# DisplayName = Arc
# Description = Generate an arc from 3 points and send commands down motion buffer to run it.
# Icon = VectorRadiusMaterialIcon
# Flags = IsProgramStep, IsHidden
# Groups = Motion

def __inputs__():
    #Description = The robot to run the vector motion with
    Inputs.Robot = new.robot("Controller0", 0)
    
    #DisplayName = Midpoint
    #Description = The mid point of the arc to be generated
    Inputs.MidPoint = new.coordinate(300, 700, 0, None, Inputs.Robot)
    
    #DisplayName = Endpoint
    #Description = The end point of the arc to be generated
    Inputs.EndPoint = new.coordinate(1000, 1000, 0, None, Inputs.Robot)
    
    #DisplayName = Is Circle
    #Description = A value indicating whether the resulting arc should close back to its start point and form a circle
    Inputs.IsCircle = new.bool(False)

    #Private = True
    #DisplayName = Begin Speed Factor
    #Description = The factor used to control the speed at the beginning of the arc vector commands
    Inputs.BeginSpeedFactor = new.double(1.00, 0, 1, 0.01, 0.1, "")

    #Private = True
    #DisplayName = End Speed Factor
    #Description = The factor used to control the speed at the end of the arc vector commands
    Inputs.EndSpeedFactor = new.double(1.00, 0, 1, 0.01, 0.1, "")

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

    if x is None:
        __throwexception__(Exceptions.AxisRequired, "X")
        return

    if y is None:
        __throwexception__(Exceptions.AxisRequired, "Y")
        return

    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    if not robot.InUseByProgram:
        robot.ResetVectorMotion()

    beginSpeed = Inputs.BeginSpeedFactor.Value * robot.VectorDispenseSpeed.Value
    endSpeed = Inputs.EndSpeedFactor.Value * robot.VectorDispenseSpeed.Value
    spacing = max(10, max(beginSpeed, endSpeed) / 250)
    bufferAmount = 50

    # Reserve an amount of buffer space for functions that don't check the available buffer space
    reserveAmount = 50

    index = 0

    # Gets all arc points, relative because of inputs
    absolutepoints = GetArcPoints(new.coordinate(0, 0, 0), Inputs.MidPoint, Inputs.EndPoint, spacing, Inputs.IsCircle.Value)

    # Get arc points as relative coordinates, removing (0,0,0) in the process
    relativepoints = RelativeMovesFromAbsolutePoints(absolutepoints)

    # Start motion with points up to buffer value
    if len(relativepoints) > 0:
        # Get the speed transition increment
        speedIncrement = (endSpeed - beginSpeed) / len(relativepoints)

        robot.InitializeVectorMotion(True)

        # Continue to fill buffer when the buffer has space
        while index < len(relativepoints):
            while (float(parseresponse(sendcommand("MG _LMS"))) < (bufferAmount + reserveAmount)):
                PVA.System.Wait(20)
            # standalone execution (controller config)
            if not robot.InUseByProgram:
                BeginVectorMotion()
            if speedIncrement == 0:
                AppendVectorLineSegmentsWithSpeed(robot, relativepoints[index:index + bufferAmount], beginSpeed)
            else:
                for point in relativepoints[index:index + bufferAmount]:
                    if speedIncrement > 0:
                        beginSpeed = beginSpeed + speedIncrement
                    AppendVectorLineSegmentWithSpeed(robot, point, beginSpeed)
                    if speedIncrement < 0:
                        beginSpeed = beginSpeed + speedIncrement
            index = index + bufferAmount

        if not robot.InUseByProgram:
            robot.WaitVectorMotionComplete()

def __virtual__():
    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    beginSpeed = Inputs.BeginSpeedFactor.Value * robot.VectorDispenseSpeed.Value
    endSpeed = Inputs.EndSpeedFactor.Value * robot.VectorDispenseSpeed.Value
    spacing = max(10, max(beginSpeed, endSpeed) / 250)
    bufferAmount = 50

    index = 0

    # Gets all arc points, relative because of inputs
    absolutepoints = GetArcPoints(new.coordinate(0, 0, 0), Inputs.MidPoint, Inputs.EndPoint, spacing, Inputs.IsCircle.Value)

    # Get arc points as relative coordinates, removing (0,0,0) in the process
    relativepoints = RelativeMovesFromAbsolutePoints(absolutepoints)

    if len(relativepoints) > 0:
        # Get the speed transition increment
        speedIncrement = (endSpeed - beginSpeed) / len(relativepoints)

        robot.InitializeVectorMotion(True)
        # standalone execution (controller config)
        if robot.InUseByProgram:
            BeginVectorMotion()

        while index < len(relativepoints):
            if speedIncrement == 0:
                AppendVectorLineSegmentsWithSpeed(robot, relativepoints[index:index + bufferAmount], beginSpeed)
            else:
                for point in relativepoints[index:index + bufferAmount]:
                    if speedIncrement > 0:
                        beginSpeed = beginSpeed + speedIncrement
                    AppendVectorLineSegmentWithSpeed(robot, point, beginSpeed)
                    if speedIncrement < 0:
                        beginSpeed = beginSpeed + speedIncrement
            index = index + bufferAmount

        if not robot.InUseByProgram:
            robot.WaitVectorMotionComplete()

def parseresponse(command):
    return command.split("\r\n")[0].strip()

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)

    return response

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
    SendAndReceive("CAS;CSS", False)

def __exceptionrecovery__():
    pass
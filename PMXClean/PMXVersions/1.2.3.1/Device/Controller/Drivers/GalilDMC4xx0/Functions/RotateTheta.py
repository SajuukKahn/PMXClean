#DisplayName = Rotate Theta
#Description = Rotate a tool in place to a specific theta position
#Icon = OrbitMaterialIcon
#Flags = IsHidden

def __inputs__():
    #Description = The robot used to move XY & Theta
    Inputs.Robot = new.robot("Controller0", 0)

    #Description = The position to rotate to
    Inputs.Position = new.position(0, Inputs.Robot, 3)

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

    toolOffset = robot.GetToolOffset()
    tool = robot.GetTool()
    x = robot.XAxis
    y = robot.YAxis
    z = robot.ZAxis
    theta = robot.ThetaAxis
    point = Inputs.Position.Value
    
    if toolOffset is None:
        __throwexception__(Exceptions.ToolRequired)
        return

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

    waitmotioncomplete(x, y, z, theta)

    if theta.Position.Value != point:
        increment = max(10, Inputs.Speed.Value / 250)
        absolutepoints = []
        startPosition = [x.Position.Value, y.Position.Value, z.Position.Value, theta.Position.Value]
        start = theta.Position.Value
        curr = start

        fl = theta.ForwardLimit.Value
        bl = theta.ReverseLimit.Value
        position = max(min(point, fl), bl)

        if start > position:
            increment = -increment

        bufferAmount = 50 # Can't be more than the total buffer size
        prepath(x, y, z, theta)
        begin = True
        for i in range(int(abs((start - position) / increment))):
            curr = curr + increment
            absolutepoints.append(rotateposition(startPosition[:], curr, toolOffset))
            if len(absolutepoints) >= bufferAmount:
                if begin:
                    absolutepoints.insert(0, startPosition[:])
                relativepoints = RelativeMovesFromAbsolutePoints(absolutepoints)
                path(begin, False, relativepoints, x, y, z, theta)
                begin = False
                last = absolutepoints[-1]
                absolutepoints = [[float(round(last[0])), float(round(last[1])), float(round(last[2])), float(round(last[3]))]]

        if begin:
            absolutepoints.insert(0, startPosition[:])
        absolutepoints.append(rotateposition(startPosition[:], position, toolOffset))
        relativepoints = RelativeMovesFromAbsolutePoints(absolutepoints)
        path(begin, True, relativepoints, x, y, z, theta)

def __virtual__():
    pass

def rotateposition(position, rotateTo, toolOffset):
    offsetDelta = toolOffset.GetOffsetDelta(rotateTo, position[3]).Point4D()
    position[0] = position[0] + offsetDelta.X
    position[1] = position[1] + offsetDelta.Y
    position[2] = position[2] + offsetDelta.Z
    position[3] = rotateTo
    return position

def path(begin, end, relativepoints, *axes):
    # Start motion with points up to buffer value
    if len(relativepoints) > 0:
        index = 0
        while (float(parseresponse(SendAndReceive("MG_LMS", False))) < len(relativepoints)):
            PVA.System.Wait(50)

        for point in relativepoints:
            move = ["" for i in range(8)]
            for i in range(len(axes)):
                move[axes[i].GetIndex()] = str(int(point[i]))
            sendcommand("LI" + ",".join(move))
            index += 1

        if begin:
            sendcommand("BGS")
            sendcommand("LE")

        # Notify controller that was the end
        if end:
            waitmotioncomplete(*axes)
            waitsettle(*axes)

def prepath(*axes):
    sendcommand("CAS")
    sendcommand("CSS")
    sendcommand("LM" + "".join([axis.GetReferenceName() for axis in axes]))
    sendcommand("VS" + str(int(Inputs.Speed.Value)))
    sendcommand("VA" + str(int(Inputs.Accel.Value)))
    sendcommand("VD" + str(int(Inputs.Decel.Value)))

def waitmotioncomplete(*axes):
    if axes is not None:
        WaitMotionComplete(axes)

def waitsettle(*axes):
    if axes is not None:
        InternalWaitSettle(axes, 0, 10)

def sendcommands(commands):
    return list(map(sendcommand, commands))

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

    return parseresponse(response)

def parseresponse(command):
    return command.split("\r\n")[0].strip()

def __outputs__():
    pass

def __lockresources__():
    PVA.Safety.SetBypassOK(False)
    if Inputs.Robot is not None:
        Inputs.Robot.Reserve()

def __releaseresources__():
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
    PVA.Safety.ResetBypassOK()

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotNotReady = new.exception("#Controller.Exceptions.RobotNotReadyTitle", "#Controller.Exceptions.RobotNotReady", new.enum("Severity", "Error").Value, None)
    Exceptions.ToolRequired = new.exception("#Tool.Exceptions.NoToolTitle", "#Tool.Exceptions.NoTool", new.enum("Severity", "Error").Value, None)
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
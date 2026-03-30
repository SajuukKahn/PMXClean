#DisplayName = Burn Robot / Log Data
#Icon = FireMaterialIcon
#Flags = IsHidden
#Groups = Motion

zFailed = 0
thetaFailed = 0
xFailed = 0
yFailed = 0
zExpected = 0
thetaExpected = 0
xExpected = 0
yExpected = 0
burnCoordinate = None

def __inputs__():
    Inputs.Robot = new.robot("Controller0", 0)
    Inputs.StartCoordinate = new.coordinate(0, 0, 0, None, Inputs.Robot)
    Inputs.XYSpeed = new.int(100000, 2, 2000000, 100, 1000, "[Unit]/s", Inputs.Robot)
    Inputs.ZSpeed = new.int(50000, 2, 1000000, 100, 1000, "[Unit]/s", Inputs.Robot)
    Inputs.ThetaSpeed = new.int(100000, 2, 1000000, 100, 1000, "[Unit]/s", Inputs.Robot, 3)
    Inputs.File = new.file()
    Inputs.LogAfter = new.int(50, 1, 1000, 10, 100, "cycles")
    Inputs.Tolerance = new.int(6, 1, 100, 1, 10, "counts")
    Inputs.AllowedFailures = new.int(1, 1, 50, 1, 10)
    Inputs.RunCount = new.int(1, 1, 100000, 10, 100, "cycles")

def __run__():
    global zFailed
    global thetaFailed
    global xFailed
    global yFailed
    global zExpected
    global thetaExpected
    global xExpected
    global yExpected
    global startCount
    global burnCoordinate

    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    x = robot.XAxis
    y = robot.YAxis
    z = robot.ZAxis
    theta = robot.ThetaAxis

    if x is None:
        __throwexception__(Exceptions.XAxisRequired)
        return

    if y is None:
        __throwexception__(Exceptions.YAxisRequired)
        return

    if z is None:
        __throwexception__(Exceptions.ZAxisRequired)
        return

    runCount = Inputs.RunCount.Value
    
    # move the robot all over:
    MoveToSafeZ(robot)
    if burnCoordinate is None:
        burnCoordinate = new.coordinate(0, 0, 0, None, robot)
    
    InternalSetAxisSpeed(x, Inputs.XYSpeed.Value)
    InternalSetAxisSpeed(y, Inputs.XYSpeed.Value)
    InternalSetAxisSpeed(z, Inputs.ZSpeed.Value)

    if theta is not None:
        InternalSetAxisSpeed(theta, Inputs.ThetaSpeed.Value)

    offLimit = 200
    # curl material lines if theta exists:
    if theta is not None:
        burnCoordinate.SetEnables(False, False, False, True)
        burnCoordinate.Theta.Value = theta.ForwardLimit.Value - offLimit
        InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)

    xSteps = subdivide(x.ReverseLimit.Value + offLimit, x.ForwardLimit.Value - offLimit, 6)
    ySteps = subdivide(y.ReverseLimit.Value + offLimit, y.ForwardLimit.Value - offLimit, 6)
    zSteps = subdivide(z.ReverseLimit.Value + offLimit, z.ForwardLimit.Value - offLimit, 5)

    burnCoordinate.Z.Value = 0
    burnCoordinate.Theta.Value = 0
    burnCoordinate.SetEnables(True, True, False, False)
    steppin = True
    robot.VectorMotionSpeed.Value = Inputs.XYSpeed.Value
    
    for step in xSteps[::-1]:
        xRelative = step - x.Position.Value
        yRelative =  ySteps[0 if steppin else -1] - y.Position.Value
        burnCoordinate.X.Value = xRelative
        burnCoordinate.Y.Value = yRelative
        move(robot, burnCoordinate)
        steppin ^= True

    for step in ySteps:
        xRelative = xSteps[0 if steppin else -1] - x.Position.Value
        yRelative = step - y.Position.Value
        burnCoordinate.X.Value = xRelative
        burnCoordinate.Y.Value = yRelative
        move(robot, burnCoordinate)
        steppin ^= True

    # move to start coordinate
    MoveToSafeZ(robot)
    burnCoordinate.X.Value = Inputs.StartCoordinate.X.Value
    burnCoordinate.Y.Value = Inputs.StartCoordinate.Y.Value
    InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)

    # z-steps, top to low1, low2, low3... then bottom back up
    burnCoordinate.SetEnables(False, False, True, False)
    
    for step in zSteps[1::]:
        burnCoordinate.Z.Value = zSteps[0]
        InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)
        burnCoordinate.Z.Value = step
        InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)
        
    for step in zSteps[-2::-1]:
        burnCoordinate.Z.Value = zSteps[-1]
        InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)
        burnCoordinate.Z.Value = step
        InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)

    MoveToSafeZ(robot)

    # theta (if theta exists)
    if theta is not None:
        burnCoordinate.SetEnables(False, False, False, True)
        thetaSteps = subdivide(theta.ReverseLimit.Value + offLimit, theta.ForwardLimit.Value - offLimit, 5)

        for step in thetaSteps:
            burnCoordinate.Theta.Value = thetaSteps[0]
            InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)
            burnCoordinate.Theta.Value = step
            InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)

        for step in thetaSteps[::-1]:
            burnCoordinate.Theta.Value = thetaSteps[-1]
            InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)
            burnCoordinate.Theta.Value = step
            InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)

        MoveToSafeZ(robot)

    if runCount >= Inputs.LogAfter.Value:
        firstTime = runCount == Inputs.LogAfter.Value
        
        burnCoordinate.X.Value = -(x.CountsPerMM.Value * 5) if x.HomeForward.Value else (x.CountsPerMM.Value * 5)
        burnCoordinate.Y.Value = -(y.CountsPerMM.Value * 5) if y.HomeForward.Value else (y.CountsPerMM.Value * 5)
        burnCoordinate.Z.Value = -(z.CountsPerMM.Value * 5) if z.HomeForward.Value else (z.CountsPerMM.Value * 5)
        
        burnCoordinate.SetEnables(False, False, True, False)
        InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)

        if theta is not None:
            burnCoordinate.Theta.Value = 0
            burnCoordinate.SetEnables(False, False, False, True)
            InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)

        if firstTime:
            zEdge = 0
            thetaEdge = 0
            xEdge = 0
            yEdge = 0
            zFailed = 0
            thetaFailed = 0
            xFailed = 0
            yFailed = 0

        # Define constant values
        xyHomeSpeed = 800
        xyTravelSpeed = 18000
        zHomeSpeed = 300
        zTravelSpeed = 7000
        maxint = 2147483647
        minint = -2147483648

        if theta is not None:
            prw = prw = theta.CountsPerDegree.Value * 320
            thetaHomeSpeed = theta.CountsPerDegree.Value
            thetaTravelSpeed = theta.CountsPerDegree.Value * 50.0

        # Get Z ready to be homed
        setlimits(minint, maxint, z)
        setdefaultaccel(z)
        setdefaultdecel(z)
        servo(z)

        # Z Home Sequence
        home(zHomeSpeed, zTravelSpeed, z)

        if not firstTime:
            zEdge = z.Position.Value - zExpected
            if abs(zEdge) > Inputs.Tolerance.Value:
                zFailed += 1
                if zFailed > Inputs.AllowedFailures.Value:
                    Exceptions.ZAxisFailure.ExceptionData.MessageParams = tuple([zEdge, z.GetDisplayName()])
                    __throwexception__(Exceptions.ZAxisFailure)
        else:
            zA1 = z.Position.Value
            home(zHomeSpeed, zTravelSpeed, z)
            zA2 = z.Position.Value
            home(zHomeSpeed, zTravelSpeed, z)
            zExpected = int((zA1 + zA2 + z.Position.Value) / 3)

        setdefaultlimits(z)

        if theta is not None:
            # Get Theta ready to be homed
            setlimits(minint, maxint, theta)
            setdefaultaccel(theta)
            setdefaultdecel(theta)
            servo(theta)

            # Theta Home Sequence
            home(thetaHomeSpeed, thetaTravelSpeed, theta)

            if not firstTime:
                thetaEdge = theta.Position.Value - thetaExpected
                if abs(thetaEdge) > (Inputs.Tolerance.Value * 5):
                    thetaFailed += 1
                    if thetaFailed > Inputs.AllowedFailures.Value:
                        Exceptions.ThetaAxisFailure.ExceptionData.MessageParams = tuple([thetaEdge, theta.GetDisplayName()])
                        __throwexception__(Exceptions.ThetaAxisFailure)
            else:
                thetaA1 = theta.Position.Value
                home(thetaHomeSpeed, thetaTravelSpeed, theta)
                thetaA2 = theta.Position.Value
                home(thetaHomeSpeed, thetaTravelSpeed, theta)
                thetaExpected = int((thetaA1 + thetaA2 + theta.Position.Value) / 3)

            #Back Off Home Sensor (Needed for material line catching)
            InternalSetAxisSpeed(theta, Inputs.ThetaSpeed.Value)
            sendcommand("PR" + theta.GetReferenceName() + "=" + str(int(prw)))
            sendcommand("BG" + theta.GetReferenceName())
            WaitMotionComplete(theta)
            stop(theta)
            InternalWaitSettle(theta, 0, 50)

            setdefaultlimits(theta)
            
        burnCoordinate.SetEnables(True, True, False, False)
        InternalMoveRobotToPosition(robot, burnCoordinate, 0, 0)
        
        # Get XY ready to be homed
        setlimits(minint, maxint, x, y)
        setdefaultaccel(x, y)
        setdefaultdecel(x, y)
        servo(x, y)

        # X&Y Home Sequence
        home(xyHomeSpeed, xyTravelSpeed, x, y)

        if not firstTime:
            xEdge = x.Position.Value - xExpected
            yEdge = y.Position.Value - yExpected
            if abs(xEdge) > Inputs.Tolerance.Value:
                xFailed += 1
                if xFailed > Inputs.AllowedFailures.Value:
                    Exceptions.XAxisFailure.ExceptionData.MessageParams = tuple([xEdge, x.GetDisplayName()])
                    __throwexception__(Exceptions.XAxisFailure)
            if abs(yEdge) > Inputs.Tolerance.Value:
                yFailed += 1
                if yFailed > Inputs.AllowedFailures.Value:
                    Exceptions.YAxisFailure.ExceptionData.MessageParams = tuple([yEdge, y.GetDisplayName()])
                    __throwexception__(Exceptions.YAxisFailure)
        else:
            xA1 = x.Position.Value
            yA1 = y.Position.Value
            home(xyHomeSpeed, xyTravelSpeed, x, y)
            xA2 = x.Position.Value
            yA2 = y.Position.Value
            home(xyHomeSpeed, xyTravelSpeed, x, y)
            xExpected = int((xA1 + xA2 + x.Position.Value) / 3)
            yExpected = int((yA1 + yA2 + y.Position.Value) / 3)

        setdefaultlimits(x, y)

        data = new.collection(new.keyvaluepair("", None))
        data.Collection.Add(new.keyvaluepair("X (" + x.GetDisplayName() + ")", xEdge))
        data.Collection.Add(new.keyvaluepair("Y (" + y.GetDisplayName() + ")", yEdge))
        data.Collection.Add(new.keyvaluepair("Z (" + z.GetDisplayName() + ")", zEdge))

        if theta is not None:
            data.Collection.Add(new.keyvaluepair("Theta (" + theta.GetDisplayName() + ")", thetaEdge))

        LogBurn(Inputs.File, data, new.enum("ArchiveFrequency", "None").Value)

def home(homeSpeed, travelSpeed, *axes):
    if not axes:
        return
    # find edge using travel speed for axes not on the home switch
    axesOffHome = [axis for axis in axes if not axis.HomeSwitch.Value]
    if len(axesOffHome) > 0:
        findedge(travelSpeed, *axesOffHome)
    # find edge again using travelSpeed to get it OFF the home switch
    findedge(travelSpeed, *axes)
    # find edge using homeSpeed to get leading edge
    findedge(homeSpeed, *axes)
    stop(*axes)

    InternalWaitSettle(axes, 0, 50)

def findedge(speed, *axes):
    if not axes:
        return

    for axis in axes:
        # Written as single command on purpose, though doesn't work as intended yet
        command = ""
        if axis.HomeForward.Value:
            command = "CN,1"
        else:
            command = "CN,-1"
        referenceName = axis.GetReferenceName()
        command = command + ";SP" + referenceName + "=" + str(int(speed))
        command = command + ";FE" + referenceName
        command = command + ";BG" + referenceName
        sendcommand(command)

    WaitMotionComplete(axes)
    sendcommand("CN,-1") # Reset CN,x back to configuration value so home switches are expected values

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

    return parseresponse(response)

def parseresponse(command):
    return command.split("\r\n")[0].strip()

def move(robot, point):
    if (point.X.Value != 0) or (point.Y.Value != 0) or (point.Z.Value != 0) or (point.Theta.IsEnabled and point.Theta.Value != 0):
        robot.InitializeVectorMotion(False)
        AppendVectorMoveSegment(robot, point)
        BeginVectorMotion()
        robot.WaitVectorMotionComplete()


def servo(*axes):
    if not axes:
        return
    sendcommand("SH" + "".join([a.GetReferenceName() for a in axes]))

def stop(*axes):
    if not axes:
        return
    sendcommand("ST" + "".join([a.GetReferenceName() for a in axes]))

def setdefaultaccel(*axes):
    if not axes:
        return
    for axis in axes:
        referenceName = axis.GetReferenceName()
        if referenceName == "C":
            sendcommand("AC" + referenceName + "=45000")
        else:
            sendcommand("AC" + referenceName + "=150000")

def setdefaultdecel(*axes):
    if not axes:
        return
    for axis in axes:
        referenceName = axis.GetReferenceName()
        if referenceName == "C":
            sendcommand("DC" + referenceName + "=45000")
        else:
            sendcommand("DC" + referenceName + "=150000")

def setdefaultlimits(*axes):
    if not axes:
        return
    for axis in axes:
        referenceName = axis.GetReferenceName()
        sendcommand("BL" + referenceName + "=" + str(int(axis.ReverseLimit.Value)))
        sendcommand("FL" + referenceName + "=" + str(int(axis.ForwardLimit.Value)))

def setlimits(bl, fl, *axes):
    if not axes:
        return
    for axis in axes:
        referenceName = axis.GetReferenceName()
        sendcommand("BL" + referenceName + "=" + str(int(bl)))
        sendcommand("FL" + referenceName + "=" + str(int(fl)))

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

def subdivide(n1, n2, steps):
    return list(sorted(set(round(n1 + i * (n2 - n1) / (steps - 1)) for i in range(steps))))

def __outputs__():
    pass

def __exceptions__():
    Exceptions.NoResponse = new.exception("No Response", "No Response from GalilDMC4xx0", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("No Robot", "The Robot is missing.", new.enum("Severity", "Error").Value, None)
    Exceptions.XAxisRequired = new.exception("Required Axis", "The Robot is missing the X axis.", new.enum("Severity", "Error").Value, None)
    Exceptions.YAxisRequired = new.exception("Required Axis", "The Robot is missing the Y axis.", new.enum("Severity", "Error").Value, None)
    Exceptions.ZAxisRequired = new.exception("Required Axis", "The Robot is missing the Z axis.", new.enum("Severity", "Error").Value, None)
    Exceptions.XAxisFailure = new.exception("Axis out of Tolerance", "The Robot X Axis ({1}) is out of tolerance by {0} counts", new.enum("Severity", "Error").Value, None)
    Exceptions.YAxisFailure = new.exception("Axis out of Tolerance", "The Robot Y Axis ({1}) is out of tolerance by {0} counts", new.enum("Severity", "Error").Value, None)
    Exceptions.ZAxisFailure = new.exception("Axis out of Tolerance", "The Robot Z Axis ({1}) is out of tolerance by {0} counts", new.enum("Severity", "Error").Value, None)
    Exceptions.ThetaAxisFailure = new.exception("Axis out of Tolerance", "The Robot Theta Axis ({1}) is out of tolerance by {0} counts", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    global startCount
    startCount = -1
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
    __exceptionhandling__()
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global burnCoordinate
    burnCoordinate = None

def __exceptionrecovery__():
    pass
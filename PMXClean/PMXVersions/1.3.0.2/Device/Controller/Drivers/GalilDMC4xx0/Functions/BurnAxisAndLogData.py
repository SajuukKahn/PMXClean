#DisplayName = Burn Axis / Log Data
#Icon = FireMaterialIcon
#Flags = IsHidden
#Groups = Motion

failed = 0
expected = 0
burnPosition = None

def __inputs__():
    Inputs.Robot = new.robot("Controller0", 0)
    Inputs.Axis = new.axis("Controller0")
    Inputs.Speed = new.int(100000, 2, 2000000, 100, 1000, "[Unit]/s", Inputs.Robot)
    Inputs.File = new.file()
    Inputs.LogAfter = new.int(50, 1, 1000, 10, 100, "cycles")
    Inputs.Tolerance = new.int(6, 1, 100, 1, 10, "counts")
    Inputs.AllowedFailures = new.int(1, 1, 50, 1, 10)
    Inputs.RunCount = new.int(1, 1, 100000, 10, 100, "cycles")

def __run__():
    global failed
    global expected
    global burnPosition

    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    axis = Inputs.Axis

    if axis is None:
        __throwexception__(Exceptions.AxisRequired)
        return

    runCount = Inputs.RunCount.Value

    # move the robot all over:
    MoveToSafeZ(robot)
    if burnPosition is None:
        burnPosition = new.position(0, axis)

    InternalSetAxisSpeed(axis, Inputs.Speed.Value)

    offLimit = 200

    steps = subdivide(axis.ReverseLimit.Value + offLimit, axis.ForwardLimit.Value - offLimit, 6)

    burnPosition.Value = 0
    burnPosition.IsEnabled = True

    for step in steps[1::]:
        burnPosition.Value = steps[0]
        move(axis, burnPosition)
        burnPosition.Value = step
        move(axis, burnPosition)

    for step in steps[-2::-1]:
        burnPosition.Value = steps[-1]
        move(axis, burnPosition)
        burnPosition.Value = step
        move(axis, burnPosition)

    if runCount >= Inputs.LogAfter.Value:
        firstTime = runCount == Inputs.LogAfter.Value

        burnPosition.Value = -(axis.CountsPerMM.Value * 5) if axis.HomeForward.Value else (axis.CountsPerMM.Value * 5)
        move(axis, burnPosition)

        if firstTime:
            edge = 0
            failed = 0

        # Define constant values
        homeSpeed = 800
        travelSpeed = 18000
        maxint = 2147483647
        minint = -2147483648

        # Get Z ready to be homed
        setlimits(minint, maxint, axis)
        setdefaultaccel(axis)
        setdefaultdecel(axis)
        servo(axis)

        home(homeSpeed, travelSpeed, axis)

        if not firstTime:
            edge = axis.Position.Value - expected
            if abs(edge) > Inputs.Tolerance.Value:
                failed += 1
                if failed > Inputs.AllowedFailures.Value:
                    Exceptions.AxisFailure.ExceptionData.MessageParams = tuple([edge, axis.GetDisplayName()])
                    __throwexception__(Exceptions.AxisFailure)
        else:
            a1 = axis.Position.Value
            home(homeSpeed, travelSpeed, axis)
            a2 = axis.Position.Value
            home(homeSpeed, travelSpeed, axis)
            expected = int((a1 + a2 + axis.Position.Value) / 3)

        setdefaultlimits(axis)

        data = new.collection(new.keyvaluepair("", None))
        data.Collection.Add(new.keyvaluepair("(" + axis.GetDisplayName() + ")", edge))

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

def move(axis, position):
    if (position.Value != 0):
        referenceName = axis.GetReferenceName()
        sendcommand("PA" + referenceName + "=" + str(int(position.Value)))
        sendcommand("BG" + referenceName)
        waitmotioncomplete(axis)

def waitmotioncomplete(*axes):
    if axes is not None:
        WaitMotionComplete(axes)

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
    Exceptions.AxisRequired = new.exception("Required Axis", "The Robot is missing the X axis.", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisFailure = new.exception("Axis out of Tolerance", "The Robot X Axis ({1}) is out of tolerance by {0} counts", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    global startCount
    startCount = -1
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
    __exceptionhandling__()
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
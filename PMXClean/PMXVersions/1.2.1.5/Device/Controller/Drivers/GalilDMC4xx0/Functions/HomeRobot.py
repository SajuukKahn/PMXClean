#DisplayName = Home Robot
#Description = Home a robot and establish its position
#Icon = HomeMaterialIcon
#Groups = Motion
#Flags = IsTriggerStep

readyToStart = False
dialog = "homeRobot"

def __inputs__():
    #Description = The robot to be homed
    Inputs.Robot = new.robot("Controller0", 0)

def __run__():
    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    if PVA.Safety.GetSafetyCheckComplete() is False:
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

    global readyToStart
    readyToStart = False

    if robot.IsMotionReady:
        SetHomingSignal(True)
        PVA.System.Wait(50)
        SetHomingSignal(False)
        return

    # Show Start Message
    global dialog
    PVA.Messaging.CreateDialog(dialog)
    PVA.Messaging.SetDialogIcon(dialog, "HomeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialog, "Yellow")
    PVA.Messaging.SetDialogTitle(dialog, "#Controller.HomeRobot")
    PVA.Messaging.SetDialogMessage(dialog, "Press #Messaging.OK to home " + robot.GetDisplayName())
    PVA.Messaging.SetDialogButtonProperties(dialog, 3, True, True, False, "#Messaging.OK", ready)
    PVA.Messaging.ShowDialogAsync(dialog)
    while not readyToStart:
        PVA.System.Wait(25)

    # Show In Progress Message
    PVA.Messaging.SetDialogButtonProperties(dialog, 3, False, False, False, "#Messaging.OK", None)
    PVA.Messaging.SetDialogMessage(dialog, "Homing " + robot.GetDisplayName() + ". Please Wait.")
    PVA.Messaging.SetDialogProgressBarIndeterminate(dialog, True)

    # Define constant values
    xyHomeSpeed = 200
    xyTravelSpeed = 15000
    zHomeSpeed = 100
    zTravelSpeed = 5000
    maxint = 2147483647
    minint = -2147483648

    # Get robot XYZ data
    coordinate = robot.Origin.Coordinate
    definition = robot.Origin.Definition
    prx = coordinate.X.Value
    pry = coordinate.Y.Value
    prz = coordinate.Z.Value
    dpx = definition.X.Value
    dpy = definition.Y.Value
    dpz = definition.Z.Value

    # Get robot Theta data
    if theta is not None:
        thetaHomeSpeed = theta.CountsPerDegree.Value
        thetaTravelSpeed = theta.CountsPerDegree.Value * 60.0
        prw = theta.CountsPerDegree.Value * 320
        dpw = definition.Theta.Value - coordinate.Theta.Value

    # Get XYZ ready to be homed
    setlimits(minint, maxint, x, y, z)
    setdefaultaccel(x, y, z)
    setdefaultdecel(x, y, z)
    servo(x, y, z)

    # Z Home Sequence
    home(zHomeSpeed, zTravelSpeed, z)
    # Back off Z Home Sensor
    if prz != 0:
        zReferenceName = z.GetReferenceName()
        sendcommand("PR" + zReferenceName + "=" + str(int(prz)))
        sendcommand("SP" + zReferenceName + "=" + str(int(zTravelSpeed)))
        sendcommand("BG" + zReferenceName)
        WaitMotionComplete(z)
        stop(z)
        InternalWaitSettle(z, 0, 10)
    # Define Z Position
    defineposition(dpz, z)
    setdefaultlimits(z)

    PVA.Tools.AllUp()
    SetHomingSignal(True)
    PVA.System.Wait(250)

    if theta is not None:
        # Get Theta ready to be homed
        setlimits(minint, maxint, theta)
        setdefaultaccel(theta)
        setdefaultdecel(theta)
        servo(theta)

        # Theta Home Sequence
        home(thetaHomeSpeed, thetaTravelSpeed, theta)
        # Define Theta Position
        defineposition(dpw, theta)
        setdefaultlimits(theta)
        
        theteReferenceName = theta.GetReferenceName()
        sendcommand("PR" + theteReferenceName + "=" + str(int(prw)))
        sendcommand("SP" + theteReferenceName + "=" + str(int(thetaTravelSpeed)))
        sendcommand("BG" + theteReferenceName)
        WaitMotionComplete(theta)
        stop(theta)
        InternalWaitSettle(theta, 0, 10)

    # X&Y Home Sequence
    home(xyHomeSpeed, xyTravelSpeed, x, y)
    # Back off X&Y Home Sensors
    if (prx != 0) or (pry != 0):
        xReferenceName = x.GetReferenceName()
        yReferenceName = y.GetReferenceName()
        sendcommand("PR" + xReferenceName + "=" + str(int(prx)))
        sendcommand("PR" + yReferenceName + "=" + str(int(pry)))
        sendcommand("SP" + xReferenceName + "=" + str(int(xyTravelSpeed)))
        sendcommand("SP" + yReferenceName + "=" + str(int(xyTravelSpeed)))
        sendcommand("BG" + xReferenceName + yReferenceName)
        WaitMotionComplete([x, y])
        stop(x, y)
        InternalWaitSettle([x, y], 0, 10)
    # Define X&Y Position
    defineposition(dpx, x)
    defineposition(dpy, y)
    setdefaultlimits(x, y)

    # Close Dialog
    PVA.Messaging.CloseDialog(dialog)

    PVA.Controllers.RobotHomeComplete()
    SetHomingSignal(False)

def __virtual__():
    pass

def home(homeSpeed, travelSpeed, *axes):
    if not axes:
        return
    waitOtherHomingAxes(*axes)
    for axis in axes:
        axis.IsHoming.Value = True
    # find edge using travel speed for axes not on the home switch
    axesOffHome = [axis for axis in axes if not axis.HomeSwitch.Value]
    if len(axesOffHome) > 0:
        findedge(travelSpeed, *axesOffHome)
    # find edge again using travelSpeed to get it OFF the home switch
    findedge(travelSpeed, *axes)
    # find edge using homeSpeed to get leading edge
    findedge(homeSpeed, *axes)
    stop(*axes)
    for axis in axes:
        axis.IsHomed.Value = True
        axis.IsHoming.Value = False
    InternalWaitSettle(axes, 0, 10)

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

def defineposition(position, *axes):
    if not axes:
        return
    InternalWaitSettle(axes, 0, 10)
    for axis in axes:
        sendcommand("DP" + axis.GetReferenceName() + "=" + str(int(position)))

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

def servo(*axes):
    if not axes:
        return
    sendcommand("SH" + "".join([a.GetReferenceName() for a in axes]))

def stop(*axes):
    if not axes:
        return
    sendcommand("ST" + "".join([a.GetReferenceName() for a in axes]))

def waitOtherHomingAxes(*axes):
    if not axes:
        return
    for otherAxis in GetAxes():
        for axis in axes:
            while (otherAxis.IsHoming and axis.HomeForward.Value != otherAxis.HomeForward.Value):
                PVA.System.Wait(20)

def ready():
    global readyToStart
    readyToStart = True

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
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.Robot is not None:
        Inputs.Robot.RequestMove()
        Inputs.Robot.Reserve()

def __releaseresources__():
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
        Inputs.Robot.MoveComplete()
    PVA.Safety.ResetDoorBypassOK()

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotNotReady = new.exception("#Controller.Exceptions.RobotNotReadyTitle", "#Controller.Exceptions.RobotNotReady", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialog
    if Inputs.Robot is not None:
        for axis in Inputs.Robot.GetAxes():
            if axis is not None:
                axis.IsHomed.Value = False
                axis.IsHoming.Value = False
    PVA.Messaging.CloseDialog(dialog)
    SetHomingSignal(False)

def __exceptionrecovery__():
    pass

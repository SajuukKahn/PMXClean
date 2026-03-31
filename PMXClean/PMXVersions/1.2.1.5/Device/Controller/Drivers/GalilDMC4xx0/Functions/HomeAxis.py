#DisplayName = Home Axis
#Description = Home a single axis and establish its position
#Icon = HomeMaterialIcon
#Groups = Motion
#Flags = IsTriggerStep

readyToStart = False
dialog = ""

def __inputs__():
    #Description = The axis to be homed
    Inputs.Axis = new.axis("Controller0")
    
    #DisplayName = Find Edge Speed
    #Description = The speed at which the home sensor edge will be found
    Inputs.FindEdgeSpeed = new.int(200, 0, 10000, 10, 100, "[Unit]/s", Inputs.Axis)

    #DisplayName = Show Prompts
    #Description = A value indicating whether this script should prompt before homing.
    #Private = True
    Inputs.ShowPrompts = new.bool(True)

def __run__():
    axis = Inputs.Axis

    if axis is None:
        __throwexception__(Exceptions.AxisRequired)
        return

    if axis.IsUsedByRobot:
        __throwexception__(Exceptions.CannotHome)
        return

    if axis.IsMotionReady:
        return

    if Inputs.ShowPrompts:
        global readyToStart
        global dialog
        readyToStart = False

        # Show Start Message
        dialog = PVA.Messaging.CreateUniqueDialog()
        PVA.Messaging.SetDialogIcon(dialog, "HomeMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialog, "Yellow")
        PVA.Messaging.SetDialogTitle(dialog, "#Controller.HomeAxis")
        PVA.Messaging.SetDialogMessage(dialog, "Press #Messaging.OK to home " + axis.GetDisplayName())
        PVA.Messaging.SetDialogButtonProperties(dialog, 3, True, True, False, "#Messaging.OK", ready)
        PVA.Messaging.ShowDialogAsync(dialog)
        while not readyToStart:
            PVA.System.Wait(25)

        # Show In Progress Message
        PVA.Messaging.SetDialogButtonProperties(dialog, 3, False, False, False, "#Messaging.OK", None)
        PVA.Messaging.SetDialogMessage(dialog, "Homing " + axis.GetDisplayName() + ". Please Wait.")
        PVA.Messaging.SetDialogProgressBarIndeterminate(dialog, True)

    findEdgeSpeed = Inputs.FindEdgeSpeed.Value
    if findEdgeSpeed is None:
        findEdgeSpeed = 200

    # Define constant values
    travelSpeed = axis.Speed
    maxint = 2147483647
    minint = -2147483648

    # Get axis ready to be homed
    setlimits(minint, maxint, axis)
    setdefaultaccel(axis)
    setdefaultdecel(axis)
    servo(axis)

    # Axis Home Sequence
    home(findEdgeSpeed, travelSpeed, axis)

    # Set to 0 but can be edited here if needed
    prAxis = 0
    dpAxis = 0

    # Back off Axis Home Sensor
    if prAxis != 0:
        referenceName = axis.GetReferenceName()
        sendcommand("PR" + referenceName + "=" + str(int(prAxis)))
        sendcommand("SP" + referenceName + "=" + str(int(travelSpeed)))
        sendcommand("BG" + referenceName)
        WaitMotionComplete(axis)
        stop(axis)

    # Define Axis Position
    defineposition(dpAxis, axis)
    setdefaultlimits(axis)

    # Close Dialog
    if Inputs.ShowPrompts:
        PVA.Messaging.CloseDialog(dialog)

def __virtual__():
    pass

def home(findEdgeSpeed, travelSpeed, axis):
    axis.IsHoming.Value = True
    # find edge using travel speed for axis not on the home switch
    if not axis.HomeSwitch.Value:
        findedge(travelSpeed, axis)
    # find edge again using travelSpeed to get it OFF the home switch
    findedge(travelSpeed, axis)
    # find edge using findEdgeSpeed to get leading edge
    findedge(findEdgeSpeed, axis)
    stop(axis)
    axis.IsHomed.Value = True
    axis.IsHoming.Value = False
    InternalWaitSettle(axis, 0, 10)

def findedge(speed, axis):
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

    WaitMotionComplete(axis)
    sendcommand("CN,-1") # Reset CN,x back to configuration value so home switches are expected values

def defineposition(position, axis):
    InternalWaitSettle(axis, 0, 10)
    sendcommand("DP" + axis.GetReferenceName() + "=" + str(int(position)))

def setdefaultaccel(axis):
    referenceName = axis.GetReferenceName()
    if referenceName == "C":
        sendcommand("AC" + referenceName + "=45000")
    else:
        sendcommand("AC" + referenceName + "=150000")

def setdefaultdecel(axis):
    referenceName = axis.GetReferenceName()
    if referenceName == "C":
        sendcommand("DC" + referenceName + "=45000")
    else:
        sendcommand("DC" + referenceName + "=150000")

def setdefaultlimits(axis):
    referenceName = axis.GetReferenceName()
    sendcommand("BL" + referenceName + "=" + str(int(axis.ReverseLimit.Value)))
    sendcommand("FL" + referenceName + "=" + str(int(axis.ForwardLimit.Value)))

def setlimits(bl, fl, axis):
    referenceName = axis.GetReferenceName()
    sendcommand("BL" + referenceName + "=" + str(int(bl)))
    sendcommand("FL" + referenceName + "=" + str(int(fl)))

def servo(axis):
    sendcommand("SH" + "".join(axis.GetReferenceName()))

def stop(axis):
    sendcommand("ST" + "".join(axis.GetReferenceName()))

def waitOtherHomingAxes(axis):
    for otherAxis in GetAxes():
        while (otherAxis.IsHoming and axis.HomeForward.Value != otherAxis.HomeForward.Value):
            PVA.System.Wait(20)

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

def ready():
    global readyToStart
    readyToStart = True

def __outputs__():
    pass

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.Axis is not None:
        Inputs.Axis.Reserve()

def __releaseresources__():
    if Inputs.Axis is not None:
        Inputs.Axis.Release()
    PVA.Safety.ResetDoorBypassOK()

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.CannotHome = new.exception("#Controller.Exceptions.AxisCannotHomeTitle","#Controller.Exceptions.AxisCannotHome", new.enum("Severity", "Warning").Value, None)

def __throwexception__(exception, name = ""):
    axis = Inputs.Axis
    if (axis is not None and not axis.IsUsedByRobot):
        SendAndReceive("ST" + axis.GetReferenceName(), False)
        axis.Release()
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialog
    axis = Inputs.Axis
    if (axis is not None and not axis.IsUsedByRobot):
        StopAxis(axis, True)
        axis.IsHomed.Value = False
        axis.IsHoming.Value = False
    SendAndReceive("CN,-1", False) # Reset CN,x back to configuration value so home switches are expected values
    if Inputs.ShowPrompts:
        PVA.Messaging.CloseDialog(dialog)

def __exceptionrecovery__():
    pass
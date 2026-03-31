#DisplayName = Spray Width Check
#Description = Check that the spray width is within target, and if it is not optionally adjust it to within target
#Icon = SprayWidthCustomIcon
#Flags = IsHidden

dialogName = "sprayWidthCheck"
ERROR_SUMMATION = 0
LAST_ERROR = 0
LAST_PRESSURE = 0

def __inputs__():
    #DisplayName = Spray Tool
    #Description = The spray tool to use for calibration
    Inputs.SprayTool = new.spray(0)
    
    #DisplayName = Auto Adjust
    #Description = A value indicating whether this function should auto-adjust the width to within target range
    Inputs.AutoAdjust = new.bool(True)
    
    #DisplayName = Working Distance
    #Description = The distance above the sensor where "0" is at the sensor plane
    Inputs.WorkingDistance = new.double(0, 0, 100, 0.1, 1, "[Unit]", Inputs.SprayTool, 2)
    
    #DisplayName = Target Width
    #Description = The desired width of the dipsensed material
    Inputs.TargetWidth = new.double(0, 0, 100, 0.1, 1, "[Unit]", __source__)

    #Description = The amount of tolerance off the target width is allowed
    Inputs.Tolerance = new.double(0, 0, 100, 0.1, 1, u"\u00B1[Unit]", __source__)
    
    #DisplayName = Initial Pressure
    #Description = The starting point for the pressure value
    Inputs.InitialPressure = new.double(0, 0, 100, 0.1, 1, "[Unit]", Inputs.SprayTool)
    
    #DisplayName = Auto Accept
    #Description = A value indicating whether the Width Check and subsequent possible adjustment are confirmed automatically instead of requiring user interation
    Inputs.AutoAccept = new.bool(True)
    
    #DisplayName = Failure Action
    #Description = What action to take when a failure is encountered
    Inputs.FailureAction = new.enum("FailureAction", "ThrowException")

    #Private = True
    #DisplayName = Settle Counts
    #Description = The amount of counts to settle to.
    Inputs.SettleCounts = new.double(5, 0, 50, 1, 1, "counts")

    #Private = True
    #DisplayName = Settle Time
    #Description = The minimum time to be at the given settle counts before resuming
    Inputs.SettleTime = new.double(50, 0, 5000, 1, 10, "ms")

def __run__():
    global ERROR_SUMMATION
    global LAST_ERROR
    global LAST_PRESSURE

    ERROR_SUMMATION = 0
    LAST_ERROR = 0
    LAST_PRESSURE = 0

    sprayTool = Inputs.SprayTool
    tool = sprayTool.GetTool().API

    if tool is None or sprayTool is None:
        __throwexception__(Exceptions.ToolRequired)

    if Settings.Analog is None:
        __throwexception__(Exceptions.AnalogInputMissing)
        return

    if not GetIsCalibrated():
        __throwexception__(Exceptions.SensorNotCalibrated)
        return

    if Inputs.TargetWidth < sprayTool.MinimumWidth.Value or Inputs.TargetWidth > sprayTool.MaximumWidth.Value:
        __throwexception__(Exceptions.TargetWidthOutOfBounds, str(Inputs.TargetWidth.Value))
        return

    if not tool.IsOffsetTaught():
        __throwexception__(Exceptions.ToolOffsetNotTaught, tool.GetDisplayName())
        return

    robot = tool.GetRobot()
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    x = robot.XAxis
    if x is None:
        __throwexception__(Exceptions.AxisRequired, "X")
        return

    y = robot.YAxis
    if y is None:
        __throwexception__(Exceptions.AxisRequired, "Y")
        return

    z = robot.ZAxis
    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    theta = robot.ThetaAxis

    location = robot.SprayWidthReferenceLocation
    if not location.XYLocationHasBeenTaught or not location.ZLocationHasBeenTaught:
        __throwexception__(Exceptions.ReferenceLocationNotTaught, "Spray Width Reference")
        return

    location = location.Coordinate
    controller = robot.GetController()
    if controller is None:
        __throwexception__(Exceptions.RobotRequired)
        return
        

    global dialogName
    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogIcon(dialogName, "SprayWidthCustomIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
    PVA.Messaging.SetDialogTitle(dialogName, "#SprayWidth.SprayWidth")
    PVA.Messaging.SetDialogMessage(dialogName, "#SprayWidth.SettingInitialPressure\n\n#UI.PleaseWait")
    PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
    PVA.Messaging.ShowDialogAsync(dialogName)
    PVA.SprayWidth.SetPressure(sprayTool, Inputs.InitialPressure.Value)
    
    if Inputs.AutoAdjust.Value:
        PVA.Messaging.SetDialogTitle(dialogName, "#SprayWidth.Adjust")
        PVA.Messaging.SetDialogMessage(dialogName, "#SprayWidth.PerformingSprayWidth " + tool.GetDisplayName() + ".\n\n#UI.PleaseWait")
    else:
        PVA.Messaging.SetDialogTitle(dialogName, "#SprayWidth.Check")
        PVA.Messaging.SetDialogMessage(dialogName, "#SprayWidth.PerformingSprayCheck " + tool.GetDisplayName() + ".\n\n#UI.PleaseWait")

    controller.MoveToSafeZ(robot)
    PVA.Tools.AllUp()
    controller.SetLocationSpeeds(robot, robot.SprayWidthReferenceLocation)

    controller.MoveRobotToPosition(robot, new.coordinate(None, None, None, sprayTool.ThetaPosition.Value), Inputs.SettleCounts, Inputs.SettleTime)
    location = location + tool.GetOffset(sprayTool.ThetaPosition.Value)

    controller.MoveRobotToPosition(robot, new.coordinate(location.X.Value, location.Y.Value, None, None), Inputs.SettleCounts, Inputs.SettleTime)

    tool.TryExecuteFunction("Down")

    if sprayTool.RotateToB:
        tool.TryExecuteFunction("RotateB")

    controller.MoveRobotToPosition(robot, new.coordinate(None, None, location.Z.Value + Inputs.WorkingDistance.Value, None), Inputs.SettleCounts, Inputs.SettleTime)

    width = 0
    pressure = Inputs.InitialPressure.Value
    LAST_PRESSURE = pressure;
    widthLowBound = Inputs.TargetWidth.Value - Inputs.Tolerance.Value
    widthHighBound = Inputs.TargetWidth.Value + Inputs.Tolerance.Value

    totalAdjustments = 0
    message = "Spray Check Complete:\n\nSet Width: " + "{:.2f}mm\n".format(Inputs.TargetWidth.Value)

    if Inputs.AutoAdjust.Value:
        if PVA.SprayWidth.ToolHasPressureDevice(sprayTool):
            while (width < widthLowBound or width > widthHighBound) and totalAdjustments < 10:
                pressure = adjustPressure(sprayTool, pressure, width, widthLowBound, widthHighBound)
                width = performCheck(sprayTool, tool)
                totalAdjustments += 1
        else:
            __throwexception__(Exceptions.MissingE2PRegulator)
            return
    else:
        width = performCheck(sprayTool, tool)

    if width < widthLowBound or width > widthHighBound:
        __throwexception__(Exceptions.CurrentWidthOutOfRange, str(width))
        return

    message += "Actual Width: {:.2f}mm\n".format(width) + "Pressure: {:.2f}psi".format(LAST_PRESSURE)
    
    PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, False)
    PVA.Messaging.SetDialogMessage(dialogName, message)
    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
    
    if sprayTool.RotateToB:
        tool.TryExecuteFunction("RotateA")

    tool.TryExecuteFunction("Up")

    controller.MoveToSafeZ(robot)

    if Inputs.AutoAccept.Value:
        PVA.Messaging.SetDialogTimeout(dialogName, 10000)

    while not PVA.Messaging.CheckDialogInteraction(dialogName):
        PVA.System.Wait(25)

    PVA.SprayWidth.RecordFormula(sprayTool, Inputs.WorkingDistance.Value, width, Inputs.Tolerance.Value, LAST_PRESSURE)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AnalogInputMissing = new.exception("#IO.Exceptions.AnalogInputMissingTitle", "#IO.Exceptions.AnalogInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorNotCalibrated = new.exception("#Sensor.Exceptions.SensorNotCalibratedTitle", "#Sensor.Exceptions.SensorNotCalibrated", new.enum("Severity", "Warning").Value, None)
    Exceptions.TargetWidthOutOfBounds = new.exception("#SprayWidth.Exceptions.TargetOutOfBoundsTitle", "#SprayWidth.Exceptions.TargetOutOfBounds", new.enum("Severity", "Error").Value, None)
    Exceptions.CurrentWidthOutOfRange = new.exception("#SprayWidth.Exceptions.CurrentWidthOutOfRangeTitle", "#SprayWidth.Exceptions.CurrentWidthOutOfRange", new.enum("Severity", "Error").Value, None)
    Exceptions.ToolRequired = new.exception("#Tool.Exceptions.NoToolTitle", "#Tool.Exceptions.NoTool", new.enum("Severity", "Error").Value, None)
    Exceptions.ToolOffsetNotTaught = new.exception("#Tool.Exceptions.ToolNotCalibratedTitle", "#Tool.Exceptions.ToolNotCalibrated", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.ReferenceLocationNotTaught = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotTaught", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.MissingE2PRegulator = new.exception("#SprayWidth.Exceptions.MissingE2PRegulatorTitle", "#SprayWidth.Exceptions.MissingE2PRegulator", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)

def __exceptionrecovery__():
    pass

def __lockresources__():
    if Inputs.SprayTool.GetTool().API.GetRobot() is not None:
        Inputs.SprayTool.GetTool().API.GetRobot().Reserve()

def __releaseresources__():
    if Inputs.SprayTool.GetTool().API.GetRobot() is not None:
        Inputs.SprayTool.GetTool().API.GetRobot().Release()

def performCheck(sprayTool, tool):
    tool.TryExecuteFunction("On")
    readings = []
    PVA.System.Wait(1000)

    for i in range(10):
        PVA.System.Wait(50)
        readings.append(_PollReading_.Reading.Value)

    tool.TryExecuteFunction("Off")
    return float(sum(readings) / float(len(readings)))


def adjustPressure(sprayTool, pressure, width, widthLowBound, widthHighBound):
    global ERROR_SUMMATION
    global LAST_ERROR
    global LAST_PRESSURE

    proportional = 1
    integral = .2
    derivative = .75
    proportionalTerm = 0

    if width == 0:
        PVA.SprayWidth.SetPressure(sprayTool, pressure)
        LAST_PRESSURE = pressure
        return LAST_PRESSURE

    targetWidth = (widthLowBound + widthHighBound) / 2

    error = targetWidth - width
    ERROR_SUMMATION += (error * integral)
    integralTerm = ERROR_SUMMATION

    if abs(error) > 0.1:
        proportionalTerm = error * proportional

    derivativeTerm = (error - LAST_ERROR) * derivative
    LAST_PRESSURE += proportionalTerm + integralTerm + derivativeTerm

    LAST_ERROR = error

    if LAST_PRESSURE < sprayTool.MinimumPressure.Value:
        LAST_PRESSURE = sprayTool.MinimumPressure.Value

    if LAST_PRESSURE > sprayTool.MaximumPressure.Value:
        LAST_PRESSURE = sprayTool.MaximumPressure.Value

    PVA.SprayWidth.SetPressure(sprayTool, LAST_PRESSURE)

    return LAST_PRESSURE
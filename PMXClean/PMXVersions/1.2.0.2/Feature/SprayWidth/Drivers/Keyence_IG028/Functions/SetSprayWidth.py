#DisplayName = Set Spray Width
#Description = Set the Spray Width using a saved Formula
#Icon = SprayWidthCustomIcon
#Flags = IsProcessStep, IsTriggerStep

dialogName = "setSprayWidth"
ERROR_SUMMATION = 0
LAST_ERROR = 0
LAST_PRESSURE = 0

def __inputs__():
    #Description = Previously accepted formula resulting in a good spray
    Inputs.Formula = new.formula()
    
    #DisplayName = Check Width
    #Description = Value indicating whether this method should check that the width is valid before continuing
    Inputs.CheckWidth = new.bool(True)
    
    #DisplayName = Adjust if Out of Range
    #Description = Value indicating whether this device should adjust the width if it is out of range as defined by the formula
    Inputs.AdjustIfOutOfRange = new.bool(True)

    #Private = True
    #DisplayName = Settle Counts
    #Description = The amount of counts to settle to
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

    formula = Inputs.Formula.FormulaReference
    sprayTool = Inputs.Formula.SprayToolReference
    tool = sprayTool.GetTool().API

    if sprayTool is None or tool is None:
        __throwexception__(Exceptions.ToolRequired)

    if Settings.Analog is None:
        __throwexception__(Exceptions.AnalogInputMissing)
        return

    if not GetIsCalibrated():
        __throwexception__(Exceptions.SensorNotCalibrated)
        return

    if formula.Width < sprayTool.MinimumWidth.Value or formula.Width > sprayTool.MaximumWidth.Value:
        __throwexception__(Exceptions.TargetWidthOutOfBounds, str(formula.Width))
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
    PVA.SprayWidth.SetPressure(sprayTool, formula.Pressure.Value)

    
    if Inputs.CheckWidth.Value:
        if Inputs.AdjustIfOutOfRange.Value:
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

        controller.MoveRobotToPosition(robot, new.coordinate(None, None, location.Z.Value + formula.WorkingDistance.Value, None), Inputs.SettleCounts, Inputs.SettleTime)

        width = 0
        pressure = formula.Pressure.Value
        LAST_PRESSURE = pressure
        widthLowBound = formula.Width.Value - formula.Tolerance.Value
        widthHighBound = formula.Width.Value + formula.Tolerance.Value

        totalAdjustments = 0

        if PVA.SprayWidth.ToolHasPressureDevice(sprayTool):
            width = performCheck(sprayTool, tool)
            if Inputs.AdjustIfOutOfRange.Value:
                while (width < widthLowBound or width > widthHighBound) and totalAdjustments < 10:
                    pressure = adjustPressure(sprayTool, pressure, width, widthLowBound, widthHighBound)
                    width = performCheck(sprayTool, tool)
                    totalAdjustments += 1
    
        if sprayTool.RotateToB:
            tool.TryExecuteFunction("RotateA")

        tool.TryExecuteFunction("Up")

        controller.MoveToSafeZ(robot)

        PVA.SprayWidth.RecordFormula(sprayTool, formula.WorkingDistance.Value, width, formula.Tolerance.Value, LAST_PRESSURE)

    PVA.Messaging.CloseDialog(dialogName)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AnalogInputMissing = new.exception("#IO.Exceptions.AnalogInputMissingTitle", "#IO.Exceptions.AnalogInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorNotCalibrated = new.exception("#Sensor.Exceptions.SensorNotCalibratedTitle", "#Sensor.Exceptions.SensorNotCalibrated", new.enum("Severity", "Warning").Value, None)
    Exceptions.TargetWidthOutOfBounds = new.exception("#SprayWidth.Exceptions.TargetOutOfBoundsTitle", "#SprayWidth.Exceptions.TargetOutOfBounds", new.enum("Severity", "Error").Value, None)
    Exceptions.ToolRequired = new.exception("#Tool.Exceptions.NoToolTitle", "#Tool.Exceptions.NoTool", new.enum("Severity", "Error").Value, None)
    Exceptions.ToolOffsetNotTaught = new.exception("#Tool.Exceptions.ToolNotCalibratedTitle", "#Tool.Exceptions.ToolNotCalibrated", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.ReferenceLocationNotTaught = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotTaught", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)

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
    if Inputs.Formula is not None:
        Inputs.Formula.SprayToolReference.GetTool().API.GetRobot().Reserve()

def __releaseresources__():
    if Inputs.Formula is not None:
        Inputs.Formula.SprayToolReference.GetTool().API.GetRobot().Release()

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
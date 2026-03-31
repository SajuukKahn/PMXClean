# DisplayName = Calibrate Sensor
# Description = Calibrate the Needle Calibration Sensors using a known good Tool offset
# Icon = CrosshairsGpsMaterialIcon
# Flags = IsHidden

dialog = "calibrateSensor"
settleCounts = new.int(0, 0, 200, 1, 10, "counts")
settleTime = new.int(50, 0, 2000, 1, 10, "ms")

def __inputs__():
    #Description = The tool used to calibrate the sensors
    Inputs.Tool = new.ncaltool(0)
    
    #DisplayName = Find Speed
    #Description = The speed used to find the sensors
    Inputs.FindSpeed = new.int(100, 10, 10000, 10, 100, "[Unit]/s", Inputs.Tool)
    
    #DisplayName = Travel Speed
    #Description = The speed used to move between sensor locations in the calibration block
    Inputs.TravelSpeed = new.int(1000, 100, 10000, 100, 1000, "[Unit]/s", Inputs.Tool)

    #Description = The maximum amount of time to spend searching for sensors
    Inputs.Timeout = new.int(10000, 500, 50000, 10, 100, "ms")
    
    #DisplayName = Sensor Finds
    #Description = The number of times each sensor must be found
    Inputs.SensorFinds = new.int(3, 1, 10, 1, 1, "")

def __run__():
    tool = Inputs.Tool
    if tool is None:
        __throwexception__(Exceptions.ToolRequired)
    if not tool.IsOnZAxis() or not tool.IsOffsetTaught():
        __throwexception__(Exceptions.ToolNeedleCannotBeCalibrated)

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

    global dialog
    PVA.Messaging.CreateDialog(dialog)
    PVA.Messaging.SetDialogIcon(dialog, "CrosshairsGpsMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialog, "Yellow")
    PVA.Messaging.SetDialogTitle(dialog, "#NeedleCalibration.CalibrateSensor")
    PVA.Messaging.SetDialogMessage(dialog, "#NeedleCalibration.Calibrating " + GetDisplayName() + " #UI.With " + tool.GetDisplayName() + ". #UI.PleaseWait.")
    PVA.Messaging.SetDialogProgressBarIndeterminate(dialog, True)
    PVA.Messaging.ShowDialogAsync(dialog)

    ClearCalibration()

    global settleCounts
    global settleTime
    results = FindSensor(Inputs.Tool, Inputs.FindSpeed, Inputs.TravelSpeed, Inputs.Timeout, Inputs.SensorFinds, settleCounts, settleTime)
    if results.Success.Value:
        xDelta = results.XDelta.Value * x.CountsPerMM.Value
        yDelta = results.YDelta.Value * y.CountsPerMM.Value
        zDelta = results.ZDelta.Value * z.CountsPerMM.Value
        Calibrate(robot, xDelta, yDelta, zDelta)

    PVA.Messaging.CloseDialog(dialog)

def __virtual__():
    pass

def __outputs__():
    pass

def __lockresources__():
    if Inputs.Tool.GetRobot() is not None:
        Inputs.Tool.GetRobot().Reserve()

def __releaseresources__():
    if Inputs.Tool.GetRobot() is not None:
        Inputs.Tool.GetRobot().Release()

def __exceptions__():
    Exceptions.ToolRequired = new.exception("#Tool.Exceptions.NoToolTitle", "#Tool.Exceptions.NoTool", new.enum("Severity", "Error").Value, None)
    Exceptions.ToolNeedleCannotBeCalibrated = new.exception("#Tool.Exceptions.CannotBeCalibratedTitle", "#Tool.Exceptions.CannotBeCalibrated", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialog
    PVA.Messaging.CloseDialog(dialog)
    if Inputs.Tool.GetRobot() is not None:
        Inputs.Tool.GetRobot().Release()

def __exceptionrecovery__():
    pass
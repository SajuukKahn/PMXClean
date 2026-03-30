#DisplayName = Shot Weight Check
#Description = Check that the shot weight is within the tolerance range
#Icon = ScaleMaterialIcon
#SubIcon = CheckBoldMaterialIcon
#Flags = IsHidden, IsTriggerStep, IsProcessStep

dialogName = ""

def __inputs__():
    #DisplayName = Shot Weight Tool
    #Description = The shot weight tool to use for the check
    Inputs.ShotTool = new.shotweighttool(0)

    #DisplayName = Target Weight
    #Description = The expected weight of the dispense shot
    Inputs.TargetWeight = new.double(0.1, 0.1, 2147483646, 0.1, 1, "[Unit]", __source__)

    #DisplayName = Dispense Time
    #Description = The amount of time to dispense the test shot
    Inputs.DispenseTime = new.double(1, 1, 2147483646, 1, 10, "ms")

    #DisplayName = Tolerance
    #Description = The amount of tolerance off the expected weight that is allowed
    Inputs.Tolerance = new.double(0.0, 0, 100, 0.1, 1, u"\u00B1%")

    #DisplayName = Error On Out-of-Range
    #Description = Whether or not to throw an error when a dispense is outside of tolerance
    Inputs.ErrorOnOutOfRange = new.bool(True)

    #DisplayName = Display Results
    #Description = Whether or not to display the results of the shot weight check
    Inputs.DisplayResults = new.bool(True)

    #Optional = True
    #DisplayName = Auto Close Results After
    #Description = The delay before automatically closing the results of the check
    Inputs.AutoCloseResultsAfter = new.int(3000, 0, 30000, 10, 100, "ms")

    #Private = True
    #DisplayName = Settle Counts
    #Description = The amount of counts to settle to
    Inputs.SettleCounts = new.double(5, 0, 50, 1, 1, "counts")

    #Private = True
    #DisplayName = Settle Time
    #Description = The minimum time to be at the given settle counts before resuming
    Inputs.SettleTime = new.double(50, 0, 5000, 1, 10, "ms")

def __run__():
    shotTool = Inputs.ShotTool
    tool = shotTool.GetTool().API

    if tool is None or shotTool is None:
        __throwexception__(Exceptions.ToolRequired)

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

    location = robot.ShotScaleReferenceLocation
    if not location.XYLocationHasBeenTaught or not location.ZLocationHasBeenTaught:
        __throwexception__(Exceptions.ReferenceLocationNotTaught, "Shot Scale Reference")
        return

    location = location.Coordinate
    controller = robot.GetController()
    if controller is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    global dialogName
    dialogName = PVA.Messaging.CreateUniqueDialog()
    PVA.Messaging.SetDialogIcon(dialogName, "ScaleMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
    PVA.Messaging.SetDialogTitle(dialogName, "#ShotScale.ShotWeight")
    PVA.Messaging.SetDialogMessage(dialogName, "#ShotScale.MovingToLocation\n\n#UI.PleaseWait")
    PVA.Messaging.ShowDialogAsync(dialogName)

    Outputs.Running.Value = True
    controller.MoveToSafeZ(robot)
    PVA.Tools.AllUp()
    controller.SetLocationSpeeds(robot, robot.ShotScaleReferenceLocation)

    location = location.Coordinate() + tool.GetOffset(shotTool.ThetaPosition.Value)
    PVA.Messaging.SetDialogMessage(dialogName, "#ShotScale.PerformingShotWeightCheck\n\n#UI.PleaseWait")
    
    controller.MoveRobotToPosition(robot, new.coordinate(location.X, location.Y, None, None), Inputs.SettleCounts, Inputs.SettleTime)
    controller.MoveRobotToPosition(robot, new.coordinate(None, None, None, shotTool.ThetaPosition.Value), Inputs.SettleCounts, Inputs.SettleTime)
    
    tool.TryExecuteFunction("Down")

    controller.MoveRobotToPosition(robot, new.coordinate(None, None, location.Z, None), Inputs.SettleCounts, Inputs.SettleTime)

    weight = 0
    lowBound = Inputs.TargetWeight.Value - (Inputs.TargetWeight.Value * (Inputs.Tolerance.Value / 100))
    highBound = Inputs.TargetWeight.Value + (Inputs.TargetWeight.Value * (Inputs.Tolerance.Value / 100))

    message = "#ShotScale.ShotWeightCheckComplete\n\n#ShotScale.TargetWeightC " + "{:.4f}g\n".format(Inputs.TargetWeight.Value)

    Tare()
    tool.TryExecuteFunction("On")
    PVA.System.Wait(Inputs.DispenseTime.Value)
    tool.TryExecuteFunction("Off")
    tool.TryExecuteFunction("Up")
    PVA.System.Wait(1000)
    weight = Read().Reading.Value

    Outputs.ShotWeight.Value = weight

    shotTool.AddWeightCheckResult(Inputs.TargetWeight.Value, weight, Inputs.DispenseTime.Value, Inputs.Tolerance.Value, GetCurrentUnit())

    if (weight < lowBound or weight > highBound):
        Outputs.Result.Value = False
    else:
        Outputs.Result.Value = True
    
    Outputs.TargetWeight.Value = Inputs.TargetWeight.Value
    Outputs.DispenseTime.Value = Inputs.DispenseTime.Value
    Outputs.Tolerance.Value = Inputs.Tolerance.Value

    if (not Outputs.Result.Value and Inputs.ErrorOnOutOfRange.Value):
        __exceptionhandling__()
        Exceptions.WeightOutOfRange.ExceptionData.MessageParams = tuple([GetDisplayName(), weight, Inputs.TargetWeight.Value, Inputs.Tolerance.Value, GetCurrentUnit()])
        PVA.Exceptions.ThrowException(Exceptions.WeightOutOfRange)

    message += "#ShotScale.ActualWeightC {:.4f}g\n".format(weight)
    
    if (Inputs.DisplayResults.Value):
        PVA.Messaging.SetDialogMessage(dialogName, message)
        PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
        if Inputs.AutoCloseResultsAfter is not None:
            PVA.Messaging.SetDialogTimeout(dialogName, Inputs.AutoCloseResultsAfter.Value)
        while not PVA.Messaging.CheckDialogInteraction(dialogName):
            PVA.System.Wait(25)

    controller.MoveToSafeZ(robot)
    Outputs.Running.Value = False
    PVA.Messaging.CloseDialog(dialogName)

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Shot Weight
    #Description = The weight of the shot dispensed
    Outputs.ShotWeight = new.double(0.0, -100, 2147483646, 0.1, 1, "[Unit]", Inputs.ShotTool)

    #Property = True
    #DisplayName = Target Weight
    #Description = The expected weight of the dispense shot
    Outputs.TargetWeight = new.double(0.0, 0, 2147483646, 0.1, 1, "[Unit]", Inputs.ShotTool)

    #Property = True
    #DisplayName = Dispense Time
    #Description = The amount of time to dispense the test shot
    Outputs.DispenseTime = new.double(0, 0, 2147483646, 1, 10, "ms")

    #Property = True
    #DisplayName = Tolerance
    #Description = The amount of tolerance off the expected weight that is allowed
    Outputs.Tolerance = new.double(0.0, 0, 100, 0.1, 1, u"\u00B1%")

    #Property = True
    #DisplayName = Shot Weight Check Result
    #Description = A value indicating whether the shot weight check passed or not
    Outputs.Result = new.bool(False, True)

    #Property = True
    #DisplayName = Is Checking
    #Description = A value indicating whether the shot weight check is actively running
    Outputs.Running = new.bool(False, True)

def __exceptions__():
    Exceptions.WeightOutOfRange = new.exception("#ShotScale.Exceptions.WeightOutOfRangeTitle", "#ShotScale.Exceptions.WeightOutOfRange\n\n #ShotScale.ActualWeightC {1:N4} {4}\n#ShotScale.TargetWeightC {2:N4} {4}\n#ShotScale.ToleranceC {3:N1}%", new.enum("Severity", "Error").Value, None)
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
    __releaseresources__()
    Outputs.Running.Value = False
    PVA.Messaging.CloseDialog(dialogName)

def __exceptionrecovery__():
    pass

def __lockresources__():
    if Inputs.ShotTool.GetTool().API.GetRobot() is not None:
        Inputs.ShotTool.GetTool().API.GetRobot().Reserve()

def __releaseresources__():
    if Inputs.ShotTool.GetTool().API.GetRobot() is not None:
        Inputs.ShotTool.GetTool().API.GetRobot().Release()
#DisplayName = Find Sensor
#Description = Find the sensors for a calibration run
#Icon = CrosshairsGpsMaterialIcon
#Flags = IsHidden

zTravelSpeedMulti = 3.0

def __inputs__():
    #Description = The tool to find the sensors with
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
    Inputs.SensorFinds = new.int(1, 1, 10, 1, 1, "")

    #Private = True
    #DisplayName = Settle Counts
    #Description = The amount of counts to settle to.
    Inputs.SettleCounts = new.double(5, 0, 50, 1, 1, "counts")

    #Private = True
    #DisplayName = Settle Time
    #Description = The minimum time to be at the given settle counts before resuming
    Inputs.SettleTime = new.double(50, 0, 5000, 1, 10, "ms")

def __run__():
    tool = Inputs.Tool

    acc = new.int(30000)
    dec = new.int(800000)
    if tool is None:
        __throwexception__(Exceptions.ToolRequired, None)
        return

    if not tool.IsOnZAxis() or not tool.IsOffsetTaught():
        __throwexception__(Exceptions.ToolNeedleCannotBeCalibrated, None)
        return

    robot = tool.GetRobot()
    if robot is None:
        __throwexception__(Exceptions.RobotRequired, None)
        return

    x = robot.XAxis
    if x is None:
        __throwexception__(Exceptions.AxisRequired, "X")
        return

    xStartDelta = -1.5 * x.CountsPerMM.Value

    y = robot.YAxis
    if y is None:
        __throwexception__(Exceptions.AxisRequired, "Y")
        return

    yStartDelta = -1.5 * y.CountsPerMM.Value

    z = robot.ZAxis
    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    zStartDelta = 2.5 * z.CountsPerMM.Value

    theta = robot.ThetaAxis

    # TODO: Make sure this sensor is the same as the robots
    #sensor = robot.GetNeedleCalibrationSensor()
    #if sensor is None:
    #    __throwexception__(Exceptions.SensorRequired, None)
    #    return

    location = robot.NeedleCalibrationReferenceLocation
    if not location.LocationHasBeenTaught:
        __throwexception__(Exceptions.ReferenceLocationNotTaught, "Needle Calibration Reference")
        return

    location = location.Coordinate
    if theta is not None and location.Theta.Value != 0:
        __throwexception__(Exceptions.ReferenceLocationBadTheta, "Needle Calibration Reference")
        return

    controller = robot.GetController()
    if controller is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    if Settings.XSensor is None:
        __throwexception__(Exceptions.SensorInputMissing, "X Sensor Input")
        return

    if CheckXState().State.Value:
        __throwexception__(Exceptions.SensorNotOff, "X ")
        return

    if Settings.YSensor is None:
        __throwexception__(Exceptions.SensorInputMissing, "Y Sensor Input")
        return

    if CheckYState().State.Value:
        __throwexception__(Exceptions.SensorNotOff, "Y ")
        return

    if Settings.ZSensor is None:
        __throwexception__(Exceptions.SensorInputMissing, "Z Sensor Input")
        return

    if CheckZState().State.Value:
        __throwexception__(Exceptions.SensorNotOff, "Z ")
        return

    controller.MoveToSafeZ(robot)
    PVA.Tools.AllUp()

    location = location + tool.GetOffset(0)
    xSensorDelta = GetXSensorDeltaInCounts(robot)
    ySensorDelta = GetYSensorDeltaInCounts(robot)
    zSensorDelta = GetZSensorDeltaInCounts(robot)

    # Move To 0 Theta
    controller.SetLocationSpeeds(robot, robot.NeedleCalibrationReferenceLocation)
    controller.SafeMoveRobotToPosition(robot, new.coordinate(None, None, None, 0), Inputs.SettleCounts, Inputs.SettleTime)

    # Move XY to find Z Sensor
    zX = location.X.Value + zSensorDelta.X.Value
    zY = location.Y.Value + zSensorDelta.Y.Value
    zZ = location.Z.Value + zSensorDelta.Z.Value
    controller.MoveRobotToPosition(robot, new.coordinate(zX, zY, None, None), Inputs.SettleCounts, Inputs.SettleTime)
    tool.TryExecuteFunction("Down")

    controller.SetAxisAccelDecel(z, acc, dec)
    findsensoronce(controller, z, "Z", False)
    centerZ = singleedgefind(controller, z, "Z", Inputs.SensorFinds.Value, True)
    zDelta = centerZ - zZ

    # Move to a temporary SafeZ
    controller.SetLocationSpeeds(robot, robot.NeedleCalibrationReferenceLocation)
    temporarySafeZ = centerZ + (5.0 * z.CountsPerMM.Value)
    controller.MoveRobotToPosition(robot, new.coordinate(None, None, temporarySafeZ, None), Inputs.SettleCounts, Inputs.SettleTime)

    # Move XYZ to find X Sensor
    xX = location.X.Value + xSensorDelta.X.Value
    xY = location.Y.Value + xSensorDelta.Y.Value
    xZ = location.Z.Value + xSensorDelta.Z.Value + zDelta
    controller.MoveRobotToPosition(robot, new.coordinate(xX + xStartDelta, xY, None, None), Inputs.SettleCounts, Inputs.SettleTime)
    controller.MoveRobotToPosition(robot, new.coordinate(None, None, xZ, None), Inputs.SettleCounts, Inputs.SettleTime)

    controller.SetAxisAccelDecel(x, acc, dec)
    centerX = dualedgefind(controller, x, "X", Inputs.SensorFinds.Value)
    xDelta = centerX - xX

    # Move XYZ
    controller.SetLocationSpeeds(robot, robot.NeedleCalibrationReferenceLocation)
    yX = location.X.Value + ySensorDelta.X.Value + xDelta
    yY = location.Y.Value + ySensorDelta.Y.Value
    yZ = location.Z.Value + ySensorDelta.Z.Value + zDelta
    controller.MoveRobotToPosition(robot, new.coordinate(yX, None, None, None), Inputs.SettleCounts, Inputs.SettleTime)
    controller.MoveRobotToPosition(robot, new.coordinate(None, yY + yStartDelta, None, None), Inputs.SettleCounts, Inputs.SettleTime)

    controller.SetAxisAccelDecel(y, acc, dec)
    centerY = dualedgefind(controller, y, "Y", Inputs.SensorFinds.Value)
    yDelta = centerY - yY

    Outputs.Success.Value = True
    Outputs.XDelta.Value = xDelta / x.CountsPerMM.Value
    Outputs.YDelta.Value = yDelta / y.CountsPerMM.Value
    Outputs.ZDelta.Value = zDelta / z.CountsPerMM.Value

    controller.SetDefaultSpeedParameters(robot)
    controller.MoveToSafeZ(robot)
    tool.TryExecuteFunction("Up")

def __virtual__():
    pass

def reset():
    Outputs.Success.Value = False
    Outputs.XDelta.Value = 0
    Outputs.YDelta.Value = 0
    Outputs.ZDelta.Value = 0

# Note: Assumes sensor is OFF at this point
def findsensoronce(controller, axis, axisName, forward):
    multi = 1.0
    if axisName == "Z":
        global zTravelSpeedMulti
        multi = zTravelSpeedMulti
    jog(controller, axis, forward, Inputs.TravelSpeed.Value * multi)
    if not waiton(axisName):
        reset()
        __throwexception__(Exceptions.SensorFailedOn, axisName)
    stop(controller, axis)

# Note: Assumes sensor is ON at this point
def singleedgefind(controller, axis, axisName, count, forward):
    positions = []
    if count == 0:
        return None
    for i in range(int(abs(count))):
        jog(controller, axis, forward, Inputs.TravelSpeed.Value)
        if not waitoff(axisName):
            reset()
            __throwexception__(Exceptions.SensorFailedOff, axisName)
            return None
        jog(controller, axis, not forward)
        if not waiton(axisName):
            reset()
            __throwexception__(Exceptions.SensorFailedOn, axisName)
            return None
        stop(controller, axis)
        positions.append(axis.Position.Value)
    stop(controller, axis)
    result = float(sum(positions) / float(len(positions)))
    return result

# Note: Assumes sensor is ON at this point
# Note: Assumes negative edge goes first
def dualedgefind(controller, axis, axisName, count):
    positions = []
    pointFromBeam = 0
    distanceFromOffToBeam = 0
    tool = Inputs.Tool
    robot = tool.GetRobot()
    off = 0.1 * axis.CountsPerMM.Value

    if count == 0:
        return None
    for i in range(int(abs(count))):
        jog(controller, axis, False, Inputs.TravelSpeed.Value)

        if not waitoff(axisName):
            reset()
            __throwexception__(Exceptions.SensorFailedOff, axisName)
            return None

        stop(controller, axis, False)
        relativeMove(controller, robot, axisName, axis.Position.Value - off)
        stop(controller, axis)
        pointFromBeam = axis.Position.Value

        #if not waitoff(axisName, True):
        #    reset()
        #    __throwexception__(Exceptions.SensorFailedOff, axisName)
        #    return None

        jog(controller, axis, True)

        if not waiton(axisName):
            reset()
            __throwexception__(Exceptions.SensorFailedOn, axisName)
            return None

        stop(controller, axis, False)
        relativeMove(controller, robot, axisName, axis.Position.Value + off)
        stop(controller, axis)

        distanceFromOffToBeam = axis.Position.Value - pointFromBeam
        positions.append(axis.Position.Value)

    relativeMove(controller, robot, axisName, axis.Position.Value + abs(distanceFromOffToBeam))

    for i in range(int(abs(count))):
        jog(controller, axis, True, Inputs.TravelSpeed.Value)
        if not waitoff(axisName):
            reset()
            __throwexception__(Exceptions.SensorFailedOff, axisName)
            return None

        stop(controller, axis, False)
        relativeMove(controller, robot, axisName, axis.Position.Value + off)
        stop(controller, axis)

        #if not waitoff(axisName, True):
        #    reset()
        #    __throwexception__(Exceptions.SensorFailedOff, axisName)
        #    return None

        jog(controller, axis, False)

        if not waiton(axisName):
            reset()
            __throwexception__(Exceptions.SensorFailedOn, axisName)
            return None

        stop(controller, axis, False)
        relativeMove(controller, robot, axisName, axis.Position.Value - off)
        stop(controller, axis)

        positions.append(axis.Position.Value)

    stop(controller, axis, False)
    result = float(sum(positions) / float(len(positions)))
    return result

def jog(controller, axis, forward, speed=None):
    if speed is None:
        speed = Inputs.FindSpeed.Value
    speed = abs(speed)
    if not forward:
        speed = -speed
    controller.JogAxis(axis, speed)

def stop(controller, axis, settle = True):
    controller.StopAxis(axis, True)
    if settle:
        controller.WaitAxisSettle(axis, new.int(2), new.int(50))

def waiton(axisName):
    if axisName == "X":
        return WaitUntilXOn(Inputs.Timeout).Passed.Value
    elif axisName == "Y":
        return WaitUntilYOn(Inputs.Timeout).Passed.Value
    elif axisName == "Z":
        return WaitUntilZOn(Inputs.Timeout).Passed.Value
    return False

def waitoff(axisName, instant = False):
    if axisName == "X":
        return WaitUntilXOff(Inputs.Timeout if not instant else new.int(0)).Passed.Value
    elif axisName == "Y":
        return WaitUntilYOff(Inputs.Timeout if not instant else new.int(0)).Passed.Value
    elif axisName == "Z":
        return WaitUntilZOff(Inputs.Timeout if not instant else new.int(0)).Passed.Value
    return False

def relativeMove(controller, robot, axisName, dist):
    if axisName == "X":
        controller.MoveRobotToPosition(robot, new.coordinate(dist, None, None, None), Inputs.SettleCounts, Inputs.SettleTime)
    elif axisName == "Y":
        controller.MoveRobotToPosition(robot, new.coordinate(None, dist, None, None), Inputs.SettleCounts, Inputs.SettleTime)
    elif axisName == "Z":
        controller.MoveRobotToPosition(robot, new.coordinate(None, None, dist, None), Inputs.SettleCounts, Inputs.SettleTime)

def __outputs__():
    #Description = A value indicating whether the sensor find application was successful
    Outputs.Success = new.bool(False)
    
    #DisplayName = X Delta
    #Description = The delta from the expected location of the center of the sensor in X
    Outputs.XDelta = new.int(0)
    
    #DisplayName = Y Delta
    #Description = The delta from the expected location of the center of the sensor in Y
    Outputs.YDelta = new.int(0)
    
    #DisplayName = Z Delta
    #Description = The delta from the expected location of the center of the sensor in Z
    Outputs.ZDelta = new.int(0)

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
    Exceptions.SensorNotOn = new.exception("#Sensor.Exceptions.IncorrectStateTitle", "#Sensor.Exceptions.SensorNotOn", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorNotOff = new.exception("#Sensor.Exceptions.IncorrectStateTitle", "#Sensor.Exceptions.SensorNotOff", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorFailedOn = new.exception("#Sensor.Exceptions.SensorTimeoutTitle", "#Sensor.Exceptions.SensorOnTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorFailedOff = new.exception("#Sensor.Exceptions.SensorTimeoutTitle", "#Sensor.Exceptions.SensorOffTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.ReferenceLocationNotTaught = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotTaught", new.enum("Severity", "Error").Value, None)
    Exceptions.ReferenceLocationBadTheta = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationInvalidTheta", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    if Inputs.Tool.GetRobot() is not None:
        Inputs.Tool.GetRobot().Release()

def __exceptionrecovery__():
    pass
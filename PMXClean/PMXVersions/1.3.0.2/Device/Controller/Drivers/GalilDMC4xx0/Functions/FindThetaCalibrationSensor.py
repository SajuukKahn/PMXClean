#DisplayName = Find Theta Calibration Sensor
#Description = Find the center of the theta calibration sensor
#Icon = HomeSearchMaterialIcon
#Flags = IsHidden
#Groups = Motion

def __inputs__():
    #Description = The robot to find the sensor with
    Inputs.Robot = new.robot("Controller0", 0)

    #Description = The sensor to find
    Inputs.Sensor = new.device("Theta Calibration Sensor" , 0)
    
    #DisplayName = Find Speed
    #Description = The speed used to find the sensors
    Inputs.FindSpeed = new.int(200, 50, 500, 10, 100, "[Unit]/s", Inputs.Robot)
    
    #DisplayName = Travel Speed
    #Description = The speed used to move between sensor read locations
    Inputs.TravelSpeed = new.int(2000, 200, 5000, 10, 100, "[Unit]/s", Inputs.Robot)

    #Description = The maximum amount of time to spend searching for sensors
    Inputs.Timeout = new.int(10000, 500, 50000, 10, 100, "ms")

def __run__():
    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    if not robot.IsMotionReady:
        __throwexception__(Exceptions.RobotNotReady)
        return

    if Inputs.Sensor is None:
        __throwexception__(Exceptions.SensorRequired, "Theta")
        return

    x = robot.XAxis
    y = robot.YAxis
    z = robot.ZAxis

    if x is None:
        __throwexception__(Exceptions.AxisRequired, "X")
        return

    if y is None:
        __throwexception__(Exceptions.AxisRequired, "Y")
        return

    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    if not waitOn(new.int(0)):
        __throwexception__(Exceptions.SensorNotOn, "Theta")
        return

    setdefaultaxisvalues(x, y, z)

    centerX = dualedgefind(x, 1)
    centerY = dualedgefind(y, 1)
    centerZ = singleedgefind(z, 1, 25, True)

    paXYZ(x, centerX, y, centerY, z, centerZ)
    centerX = dualedgefind(x, 3)
    centerY = dualedgefind(y, 3)
    centerZ = singleedgefind(z, 3, 25, True)
    Outputs.Center.X.Value = centerX
    Outputs.Center.Y.Value = centerY
    Outputs.Center.Z.Value = centerZ
    Outputs.Found.Value = True

    paXYZ(x, centerX, y, centerY, z, centerZ)

def __virtual__():
    pass

def reset():
    Outputs.Center.X.Value = 0
    Outputs.Center.Y.Value = 0
    Outputs.Center.Z.Value = 0
    Outputs.Found.Value = False

def setdefaultaxisvalues(*axes):
    for axis in axes:
        if axis is not None:
            referenceName = axis.GetReferenceName()
            sendcommand("AC" + referenceName + "=" + str(int(axis.Acceleration.Value)))
            sendcommand("DC" + referenceName + "=" + str(int(axis.Deceleration.Value)))
            sendcommand("SP" + referenceName + "=" + str(int(axis.Speed.Value)))

def waitmotioncomplete(*axes):
    if axes is not None:
        WaitMotionComplete(axes)

def waitsettle(*axes):
    if axes is not None:
        InternalWaitSettle(axes, 0, 10)

def singleedgefind(axis, count, inc, forward):
    inc = abs(inc)
    if forward:
        inc = -inc
    pos = []
    if count == 0:
        return None
    for i in range(int(abs(count))):
        jog(axis, forward, Inputs.TravelSpeed.Value)
        if not waitOff(Inputs.Timeout):
            __throwexception__(Exceptions.SensorFailedOff, None)
        PVA.System.Wait(50)
        jog(axis, not forward)
        if not waitOn(Inputs.Timeout):
            __throwexception__(Exceptions.SensorFailedOn, None)
        stop(axis)
        pos.append(axis.Position.Value)
    result = float(sum(pos) / float(len(pos)) + inc)
    pa(axis, result)
    return result

def dualedgefind(axis, count):
    pos = []
    if count == 0:
        return None
    for i in range(int(abs(count))):
        jog(axis, True, Inputs.TravelSpeed.Value)
        if not waitOff(Inputs.Timeout):
            __throwexception__(Exceptions.SensorFailedOff, None)
            return
        PVA.System.Wait(50)
        jog(axis, False)
        if not waitOn(Inputs.Timeout):
            __throwexception__(Exceptions.SensorFailedOn, None)
            return
        stop(axis)
        pos.append(axis.Position.Value)
    for i in range(int(abs(count))):
        jog(axis, False, Inputs.TravelSpeed.Value)
        if not waitOff(Inputs.Timeout):
            __throwexception__(Exceptions.SensorFailedOff, None)
            return
        PVA.System.Wait(50)
        jog(axis, True)
        if not waitOn(Inputs.Timeout):
            __throwexception__(Exceptions.SensorFailedOn, None)
            return
        stop(axis)
        pos.append(axis.Position.Value)
    result = float(sum(pos) / float(len(pos)))
    pa(axis, result)
    return result

def paXYZ(x, posX, y, posY, z, posZ):
    xReferenceName = x.GetReferenceName()
    yReferenceName = y.GetReferenceName()
    zReferenceName = z.GetReferenceName()
    sendcommand("AC" + xReferenceName + "=" + str(int(x.Acceleration.Value)))
    sendcommand("DC" + xReferenceName + "=" + str(int(x.Deceleration.Value)))
    sendcommand("AC" + yReferenceName + "=" + str(int(y.Acceleration.Value)))
    sendcommand("DC" + yReferenceName + "=" + str(int(y.Deceleration.Value)))
    sendcommand("AC" + zReferenceName + "=" + str(int(z.Acceleration.Value)))
    sendcommand("DC" + zReferenceName + "=" + str(int(z.Deceleration.Value)))
    sendcommand("PA" + xReferenceName + "=" + str(int(posX)))
    sendcommand("PA" + yReferenceName + "=" + str(int(posY)))
    sendcommand("PA" + zReferenceName + "=" + str(int(posZ)))
    sendcommand("SP" + xReferenceName + "=" + str(int(Inputs.TravelSpeed.Value)))
    sendcommand("SP" + yReferenceName + "=" + str(int(Inputs.TravelSpeed.Value)))
    sendcommand("SP" + zReferenceName + "=" + str(int(Inputs.TravelSpeed.Value)))
    sendcommand("BG" + xReferenceName + yReferenceName + zReferenceName)
    waitmotioncomplete(x, y, z)
    waitsettle(x, y, z)

def pa(axis, position):
    referenceName = axis.GetReferenceName()
    sendcommand("AC" + referenceName + "=" + str(int(axis.Acceleration.Value)))
    sendcommand("DC" + referenceName + "=" + str(int(axis.Deceleration.Value)))
    sendcommand("PA" + referenceName + "=" + str(int(position)))
    sendcommand("SP" + referenceName + "=" + str(int(Inputs.TravelSpeed.Value)))
    sendcommand("BG" + referenceName)
    waitmotioncomplete(axis)
    waitsettle(axis)

def stop(*axes):
    if not axes:
        return
    sendcommand("ST" + "".join([axis.GetReferenceName() for axis in axes]))
    waitmotioncomplete(*axes)
    waitsettle(*axes)

def servo(*axes):
    if not axes:
        return
    command = "SH"
    for axis in axes:
        if axis.Status[0].Value:
            command = command + axis.GetReferenceName()
    if len(command) > 2:
        sendcommand(command)

def jog(axis, forward, speed=None):
    if speed is None:
        speed = Inputs.FindSpeed.Value
    speed = abs(speed)
    if not forward:
        speed = -speed
    referenceName = axis.GetReferenceName()
    sendcommand("JG" + referenceName + "=" + str(int(speed)))
    sendcommand("BG" + referenceName)

def waitOn(timeout):
    return Inputs.Sensor.WaitUntilOn(timeout).Passed.Value

def waitOff(timeout):
    return Inputs.Sensor.WaitUntilOff(timeout).Passed.Value

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)

    return response

def __outputs__():
    #Description = A value indicating whether this function found the center of the sensor
    Outputs.Found = new.bool(False, True)

    #Description = The coordinate value for the center of the sensor
    Outputs.Center = new.coordinate(0, 0)

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

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotNotReady = new.exception("#Controller.Exceptions.RobotNotReadyTitle", "#Controller.Exceptions.RobotNotReady", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorRequired = new.exception("#Sensor.Exceptions.NoSensorTitle", "#Sensor.Exceptions.NoSensor", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorNotOn = new.exception("#Sensor.Exceptions.IncorrectStateTitle", "#Sensor.Exceptions.SensorNotOn", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorFailedOn = new.exception("#Sensor.Exceptions.SensorTimeoutTitle", "#Sensor.Exceptions.SensorOnTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorFailedOff = new.exception("#Sensor.Exceptions.SensorTimeoutTitle", "#Sensor.Exceptions.SensorOffTimeout", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    reset()
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    if Inputs.Robot is not None:
        InternalStopRobot(Inputs.Robot)
    MotorOff()

def __exceptionrecovery__():
    pass

#DisplayName = Set Default Speed Parameters
#Description = Set the speed, acceleration, and deceleration for all of a robot's axes back to default
#Icon = VectorRadiusMaterialIcon
#Flags = IsHidden

def __inputs__():
    #Description = The robot to restore defaults to
    Inputs.Robot = new.robot("Controller0", 0)

def __run__():
    robot = Inputs.Robot
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    for axis in robot.GetAxes():
        if axis is not None:
            referenceName = axis.GetReferenceName()
            sendcommand("AC" + referenceName + "=" + str(int(axis.Acceleration.Value)))
            sendcommand("DC" + referenceName + "=" + str(int(axis.Deceleration.Value)))
            sendcommand("SP" + referenceName + "=" + str(int(axis.Speed.Value)))

def __virtual__():
    pass

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

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = Move To Safe Z
#Description = Move a Robot to its safe Z position
#Icon = RobotSafeZCustomIcon
#Groups = Motion
#Flags = IsTriggerStep

def __inputs__():
    #Description = The robot to move
    Inputs.Robot = new.robot("Controller0", 0)

def __run__():
    robot = Inputs.Robot
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    MoveToSafeZPosition(robot, robot.SafeZ, new.bool(False))

def __virtual__():
    robot = Inputs.Robot
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

def __outputs__():
    pass

def __lockresources__():
    pass

def __releaseresources__():
    pass

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
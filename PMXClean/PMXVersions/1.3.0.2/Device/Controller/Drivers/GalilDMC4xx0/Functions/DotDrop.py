#DisplayName = Dot Drop
#Description = Turn a dispense tool on for a specified amount of time in the current location
#Icon = RadioboxMarkedMaterialIcon
#Flags = IsHidden

def __inputs__():
    #Description = The robot to dispense the dot with
    Inputs.Robot = new.robot("Controller0", 0)
    
    #DisplayName = On Dwell
    #Description = The amount of time to wait after turning the tool on
    Inputs.OnTime = new.int(100, 0, 1000000, 10, 100, "ms")

def __run__():
    robot = Inputs.Robot

    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    Inputs.Robot.TryExecuteToolOnFunction()
    PVA.System.Wait(Inputs.OnTime.Value)
    Inputs.Robot.TryExecuteToolOffFunction()

def __virtual__():
    PVA.System.Wait(Inputs.OnTime.Value)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    if Inputs.Robot is not None:
        Inputs.Robot.TryExecuteToolOffFunction()

def __exceptionrecovery__():
    pass
# DisplayName = Tool Down
# Description = Try to execute the "Down" function on the currently selected tool
# Icon = ArrowDownBoldOutlineMaterialIcon
# SubIcon = DispenseValveBoldCustomIcon
# Flags = IsMappable, IsHidden

def __inputs__():
    #Description = The robot to get the currently selected tool from
    Inputs.Robot = new.robot("Controller0", 0)

def __run__():
    if Inputs.Robot is None:
        PVA.Exceptions.ThrowException(Exceptions.RobotRequired)

    Inputs.Robot.TryExecuteToolFunction("Down")

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
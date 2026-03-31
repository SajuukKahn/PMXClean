# DisplayName = Tool Function
# Description = Try to execute a function by name on the currently selected tool
# Icon = HammerWrenchMaterialIcon
# Flags = IsMappable, IsHidden

def __inputs__():
    #Description = The robot to get the currently selected tool from
    Inputs.Robot = new.robot("Controller0", 0)
    
    #DisplayName = Tool Function
    #Description = The name of the function to attempt to execute
    Inputs.ToolFunction = new.toolfunction("Up")

def __run__():
    robot = Inputs.Robot

    if robot is None:
        PVA.Exceptions.ThrowException(Exceptions.RobotRequired)

    robot.TryExecuteToolFunction(Inputs.ToolFunction.Value)

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
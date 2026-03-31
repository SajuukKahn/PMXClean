# DisplayName = Next Tool
# Description = Increment the SelectedTool to the next in the list
# Icon = MapMarkerRightMaterialIcon
# Flags = IsMappable, IsHidden

def __inputs__():
    #Description = The robot that is changing SelectedTool
    Inputs.Robot = new.robot("Controller0", 0)

def __run__():
    robot = Inputs.Robot

    if robot is None:
        PVA.Exceptions.ThrowException(Exceptions.RobotRequired)

    try:
        robot.NextTool()
    except:
        return # no need to throw an error here

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
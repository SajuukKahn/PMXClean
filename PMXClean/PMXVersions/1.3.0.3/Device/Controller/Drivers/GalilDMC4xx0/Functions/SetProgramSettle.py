#DisplayName = Set Program Settle
#Description = Override the default settling parameters for accuracy sensitive operations
#Icon = TimerMarkerMaterialIcon
#Flags = IsHidden
#Groups = Motion

def __inputs__():
    #Private = True
    #Description = The robot to change the settling parameters on
    Inputs.Robot = new.robot("Controller0", 0)
    
    #DisplayName = Settle Counts
    #Description = The amount of counts to settle to
    Inputs.SettleCounts = new.double(0, 0, 50, 1, 1, "counts")
    
    #DisplayName = Settle Time
    #Description = The minimum time to be at the given settle counts before resuming
    Inputs.SettleTime = new.double(10, 0, 5000, 1, 10, "ms")

def __run__():
    robot = Inputs.Robot

    if robot is None:
        PVA.Exceptions.ThrowException(Exceptions.RobotRequired)
        return

    robot.SetProgramSettleParameters(Inputs.SettleCounts.Value, Inputs.SettleTime.Value)

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
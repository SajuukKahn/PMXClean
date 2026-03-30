#DisplayName = Wait Robot Settle
#Description = Wait for a robot to settle to a maximum amount of error magnitude for a minimum amount of time
#Icon = RobotIndustrialRotate90CustomIcon
#Groups = Motion
#Flags = IsHidden

def __inputs__():
    #Description = The robot to settle
    Inputs.Robot = new.robot("Controller0", 0)
    
    #Private = True
    #Description = The allowed settling error
    Inputs.Distance = new.int(0, 0, 100, 1, 10, "[Unit]", Inputs.Robot)
    
    #Private = True
    #DisplayName = Settle Time
    #Description = The minimum time to be at the given settle distance
    Inputs.SettleTime = new.double(50, 0, 5000, 1, 10, "ms")

def __run__():
    if Inputs.Robot is not None:
        InternalWaitSettle(Inputs.Robot, Inputs.Distance.Value, Inputs.SettleTime.Value)

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
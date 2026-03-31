#DisplayName = Get Robots
#Description = Get all the robots created on the machine
#Icon = AlphaRCircleOutlineMaterialIcon
#Flags = IsHidden

def __inputs__():
    pass

def __run__():
    Outputs.Robots = GetRobots()

def __virtual__():
    pass

def __outputs__():
    #Description = The list of all robots on the machine
    Outputs.Robots = [new.robot("")]

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = All Up
#Description = Call the "Rotate A" and "Up" functions on all subscribed Tools
#Icon = ArrowUpBoldOutlineMaterialIcon
#SubIcon = DispenseValveBoldCustomIcon
#IconIndex = All
#Flags = IsTriggerStep, IsQuickAction, IsProcessStep

def __inputs__():
    pass

def __run__():
    ExecuteGroupActuate("Rotate_A")
    ExecuteGroupActuate("Up")

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = All Down
#Description = Call the "Down" function on all subscribed Tools
#Icon = ArrowDownBoldOutlineMaterialIcon
#SubIcon = DispenseValveBoldCustomIcon
#IconIndex = All
#Flags = IsTriggerStep, IsProcessStep, IsQuickAction

def __inputs__():
    pass

def __run__():
    ExecuteGroupActuate("Down")

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
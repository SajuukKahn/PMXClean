#DisplayName = All Off
#Description = Call the "Off" function on all subscribed Tools
#Icon = PowerPlugOffMaterialIcon
#SubIcon = DispenseValveBoldCustomIcon
#IconIndex = All
#Flags = IsTriggerStep, IsHidden

def __inputs__():
    pass

def __run__():
    ExecuteGroupDispense("Off")

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
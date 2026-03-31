# DisplayName = All On
# Description = Call the "On" function on all subscribed Tools
# Icon = PowerPlugMaterialIcon
# SubIcon = DispenseValveBoldCustomIcon
# IconIndex = All
# Flags = IsTriggerStep, IsHidden

def __inputs__():
    pass

def __run__():
    ExecuteGroupDispense("On")

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
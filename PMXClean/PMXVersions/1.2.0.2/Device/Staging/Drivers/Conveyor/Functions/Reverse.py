#DisplayName = Reverse
#Description = Activates the conveyor in the reverse direction according to its configuration and clears all tenant scheduling
#Icon = RewindMaterialIcon
#Flags = IsMappable, IsQuickAction

def __inputs__():
    pass

def __run__():
    ResetSchedule()
    SetDirection(True)
    SetEnable(True)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
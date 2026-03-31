#DisplayName = Off
#Description = Turns off the conveyor and clears all tenant scheduling
#Icon = PowerPlugOffMaterialIcon
#Flags = IsMappable, IsQuickAction

def __inputs__():
    pass

def __run__():
    ResetSchedule()
    SetEnable(False)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __throwexception__(exception):
    __exceptionhandling__()
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
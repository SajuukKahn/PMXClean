# DisplayName = Forward
# Description = Activates the conveyor in the forward direction according to its configuration and clears all tenant scheduling
# Icon = FastForwardMaterialIcon
# Flags = IsMappable, IsQuickAction

def __inputs__():
    pass

def __run__():
    ResetSchedule()
    SetDirection(False)
    SetEnable(True)

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
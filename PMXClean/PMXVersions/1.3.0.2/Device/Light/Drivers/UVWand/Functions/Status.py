#DisplayName = Status
#Description = Monitors the status of the UV Wand
#Icon = PollMaterialIcon
#Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    pass

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Is On
    #Description = A value indicating whether the uv wand is in the "on" state
    Outputs.IsOn = new.bool(False, True)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

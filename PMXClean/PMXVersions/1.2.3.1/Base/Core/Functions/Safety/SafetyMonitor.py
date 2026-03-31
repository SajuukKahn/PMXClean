#DisplayName = Start Safety Monitor
#Description = Start the machine safety monitor loop to detect changes in safety devices
#Icon = MonitorEyeMaterialIcon
#Flags = IsHidden

def __inputs__():
    pass

def __run__():
    ForceClosedState()
    SetSafetyCheckComplete(True)
    StartSafetyMonitor()

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
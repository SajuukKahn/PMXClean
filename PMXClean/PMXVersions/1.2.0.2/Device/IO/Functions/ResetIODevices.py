#DisplayName = Reset IO Devices
#Description = Reset all outputs on all IO devices
#Icon = ReplayMaterialIcon
#SubIcon = AlarmLightMaterialIcon
#IconIndex = All
#Flags = IsTriggerStep

def __inputs__():
    pass

def __run__():
    ResetIODevices()

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
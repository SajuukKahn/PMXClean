#DisplayName = Wait For Temperature
#Description = Waits for all heaters to reach the set point
#Icon = FireMaterialIcon
#SubIcon = TimerOutlineMaterialIcon
#IconIndex = All
#Flags = IsTriggerStep, IsProcessStep

def __inputs__():
    pass

def __run__():
    WaitAllHeatersToTemp(__cancelExecution__)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

def __cancelExecution__():
    PVA.Process.CancelExecution()
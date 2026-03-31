#DisplayName = Timed Wait
#Description = Wait a minimum amount of time before continuing
#Icon = ClockEndMaterialIcon
#Flags = IsProcessStep, IsProgramStep, IsTriggerStep

def __inputs__():
    #DisplayName = Wait Time
    #Description = The minimum amount of time to wait before continuing
    Inputs.WaitTime = new.int(2000, 0, 10000, 1, 10, "ms")

def __run__():
    Wait(Inputs.WaitTime.Value)

def __virtual__():
    Wait(Inputs.WaitTime.Value)

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = Check Low Level
#Description = Check the scale level against the low threshold
#Icon = BookOpenMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

def __inputs__():
    #DisplayName = Low Level
    #Description = The low threshold for this check
    Inputs.LowLevel = new.double(50, 0, 500, 1, 10, "")

def __run__():
    Outputs.Low.Value = False

    reading = Read().Reading
    if reading is not None:
        low = reading.Value < Inputs.LowLevel.Value

        if low is True:
            Outputs.Low.Value = True
            AddLowLevelWarning(GetDisplayName())

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating whether the tank on the scale is considered "low".
    Outputs.Low = new.bool(False, True)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = Check Empty Level
#Description = Check the scale level against the empty threshold
#Icon = BookOpenMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

def __inputs__():
    #DisplayName = Empty Level
    #Description = The empty threshold for this check
    Inputs.EmptyLevel = new.double(50, 0, 500, 1, 10, "")

def __run__():
    Outputs.Empty.Value = False

    reading = Read().Reading
    if reading is not None:
        empty = reading.Value < Inputs.EmptyLevel.Value

        if empty is True:
            Outputs.Empty.Value = True
            __throwexception__(Exceptions.EmptyLevelActivated)

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating whether the tank on the scale is considered "empty".
    Outputs.Empty = new.bool(False, True)

def __exceptions__():
    Exceptions.EmptyLevelActivated = new.exception("#Scale.Exceptions.EmptyLevelTitle", "#Scale.Exceptions.EmptyLevel", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowExceptionAsync(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
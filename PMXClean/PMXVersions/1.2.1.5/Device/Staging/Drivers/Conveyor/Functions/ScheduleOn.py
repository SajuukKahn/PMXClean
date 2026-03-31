#DisplayName = Schedule On
#Description = Indicates that a tenant is entering the schedule, which will turn on or keep on the conveyor
#Icon = ClockCheckOutlineMaterialIcon
#Flags = IsHidden

def __inputs__():
    #Description = A value indicating whether to reverse the conveyor direction
    Inputs.Reverse = new.bool(False)

def __run__():
    if Settings.EnableOutput == None:
        __throwexception__(Exceptions.EnableOutputMissing, "EnableOutput")

    SetDirection(Inputs.Reverse.Value)
    IncrementSchedule()

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.EnableOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    Off()

def __exceptionrecovery__():
    pass
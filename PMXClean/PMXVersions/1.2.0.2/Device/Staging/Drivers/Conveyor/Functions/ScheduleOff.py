#DisplayName = Schedule Off
#Description = Indicates that a tenant is leaving the schedule, if no tenants exist after the delay, the conveyor will turn off
#Icon = ClockRemoveOutlineMaterialIcon
#Flags = IsHidden

def __inputs__():
    #DisplayName = Off Delay
    #Description = The time to let the conveyor continue running before turning off, used for handing off between scripts
    Inputs.OffDelay = new.int(50, 0, 2000, 1, 10, "ms")

def __run__():
    if Settings.EnableOutput == None:
        __throwexception__(Exceptions.EnableOutputMissing, "EnableOutput")

    DecrementSchedule(int(Inputs.OffDelay.Value))

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
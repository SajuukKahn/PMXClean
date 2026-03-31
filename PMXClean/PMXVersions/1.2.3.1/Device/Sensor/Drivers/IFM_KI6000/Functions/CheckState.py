#DisplayName = Check State
#Description = Check the state of the sensor
#Icon = HydraulicOilLevelMaterialIcon

def __inputs__():
    pass

def __run__():
    Outputs.State.Value = _PollState_.PolledState.Value
    Outputs.IsSettled.Value = _PollState_.IsSettled.Value
    if Settings.Input is None:
        __throwexception__(Exceptions.InputMissing)

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating the state of the sensor
    Outputs.State = new.bool(False)
    
    #DisplayName = Is Settled
    #Description = A value indicating that the state of the sensor is stable
    Outputs.IsSettled = new.bool(False)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = Check State
#Description = Check the state of the sensor
#Icon = LedOnMaterialIcon

def __inputs__():
    pass

def __run__():
    if Settings.Input is None:
        Outputs.State.Value = not Settings.OnState.Value
        __throwexception__(Exceptions.InputMissing)

    Outputs.State.Value = Settings.Input.Value == Settings.OnState.Value

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating the state of the sensor
    Outputs.State = new.bool(False, True)

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
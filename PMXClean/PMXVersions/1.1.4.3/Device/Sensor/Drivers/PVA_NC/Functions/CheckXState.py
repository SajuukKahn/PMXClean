# DisplayName = Check X State
# Description = Check the state of the X sensor
# Icon = LedOnMaterialIcon
# Flags = IsHidden

def __inputs__():
    pass

def __run__():
    if Settings.XSensor is None:
        Outputs.State.Value = not Settings.XSensorOnState.Value
        __throwexception__(Exceptions.InputMissing)
        return
    Outputs.State.Value = Settings.XSensor.Value == Settings.XSensorOnState.Value

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating the state of the X Sensor
    Outputs.State = new.bool(False)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple(["XSensor"])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
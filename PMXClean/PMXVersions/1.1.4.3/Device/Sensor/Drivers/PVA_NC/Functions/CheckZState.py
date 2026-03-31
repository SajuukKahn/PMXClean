# DisplayName = Check Z State
# Description = Check the state of the Z sensor
# Icon = LedOnMaterialIcon
# Flags = IsHidden

def __inputs__():
    pass

def __run__():
    if Settings.ZSensor is None:
        Outputs.State.Value = not Settings.ZSensorOnState.Value
        __throwexception__(Exceptions.InputMissing)
        return
    Outputs.State.Value = Settings.ZSensor.Value == Settings.ZSensorOnState.Value

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating the state of the Z Sensor
    Outputs.State = new.bool(False)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple(["ZSensor"])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
# DisplayName = Check Y State
# Description = Check the state of the Y sensor
# Icon = LedOnMaterialIcon
# Flags = IsHidden

def __inputs__():
    pass

def __run__():
    if Settings.YSensor is None:
        Outputs.State.Value = not Settings.YSensorOnState.Value
        __throwexception__(Exceptions.InputMissing)
        return
    Outputs.State.Value = Settings.YSensor.Value == Settings.YSensorOnState.Value

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating the state of the Y Sensor
    Outputs.State = new.bool(False)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple(["YSensor"])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
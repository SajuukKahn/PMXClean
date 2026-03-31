# DisplayName = Poll State
# Description = Get the polled state of each of the needle cal sensors
# Icon = PollMaterialIcon
# Flags = IsPolling, IsHidden

thrownX = False
thrownY = False
thrownZ = False

def __inputs__():
    pass

def __run__():
    global thrownX
    global thrownY
    global thrownZ

    if Settings.XSensor is None:
        Outputs.XState.Value = not Settings.XSensorOnState.Value
        if thrownX:
            return
        thrownX = True
        __throwexception__(Exceptions.SensorInputMissing, "X Sensor Input")
    else:
        thrownX = False
        Outputs.XState.Value = Settings.XSensor.Value == Settings.XSensorOnState.Value

    if Settings.YSensor is None:
        Outputs.YState.Value = not Settings.YSensorOnState.Value
        if thrownY:
            return
        thrownY = True
        __throwexception__(Exceptions.SensorInputMissing, "Y Sensor Input")
    else:
        thrownY = False
        Outputs.YState.Value = Settings.YSensor.Value == Settings.YSensorOnState.Value

    if Settings.ZSensor is None:
        Outputs.ZState.Value = not Settings.ZSensorOnState.Value
        if thrownZ:
            return
        thrownZ = True
        __throwexception__(Exceptions.SensorInputMissing, "Z Sensor Input")
    else:
        thrownZ = False
        Outputs.ZState.Value = Settings.ZSensor.Value == Settings.ZSensorOnState.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = X State
    #Description = A value indicating the state of the X Sensor
    Outputs.XState = new.bool(False)

    #Property = True
    #DisplayName = Y State
    #Description = A value indicating the state of the Y Sensor
    Outputs.YState = new.bool(False)

    #Property = True
    #DisplayName = Z State
    #Description = A value indicating the state of the Z Sensor
    Outputs.ZState = new.bool(False)

def __exceptions__():
    Exceptions.SensorInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
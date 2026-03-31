#DisplayName = Check Low Level Sensor
#Description = Check the sensor for low level status
#Icon = BookOpenMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

def __inputs__():
    pass

def __run__():
    Outputs.Low.Value = False

    stateParameter = CheckState().State
    if stateParameter is not None:
        if stateParameter.Value is True:
            Outputs.Low.Value = True
            __throwexception__(Exceptions.LowLevelActivated)
        elif stateParameter.Value is False:
            Outputs.Low.Value = False

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating that the sensor is reading low
    Outputs.Low = new.bool(False)

def __exceptions__():
    Exceptions.LowLevelActivated = new.exception("#Sensor.Exceptions.LowLevelTriggeredTitle", "#Sensor.Exceptions.LowLevelTriggered", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowExceptionAsync(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
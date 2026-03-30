#DisplayName = Check State
#Description = Check the state of the sensor
#Icon = HydraulicOilLevelMaterialIcon

def __inputs__():
    pass

def __run__():
    if Settings.Analog is None:
        __throwexception__(Exceptions.AnalogInputMissing)
        return

    if not GetIsCalibrated():
        __throwexception__(Exceptions.SensorNotCalibrated)
        return

    Outputs.State.Value = _PollState_.PolledState.Value
    Outputs.IsSettled.Value = _PollState_.IsSettled.Value

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating the state of the sensor
    Outputs.State = new.bool(False, True)
    
    #DisplayName = Is Settled
    #Description = A value indicating that the state of the sensor is stable
    Outputs.IsSettled = new.bool(False, True)

def __exceptions__():
    Exceptions.AnalogInputMissing = new.exception("#IO.Exceptions.AnalogInputMissingTitle", "#IO.Exceptions.AnalogInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.SensorNotCalibrated = new.exception("#Sensor.Exceptions.SensorNotCalibratedTitle", "#Sensor.Exceptions.SensorNotCalibrated", new.enum("Severity", "Warning").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
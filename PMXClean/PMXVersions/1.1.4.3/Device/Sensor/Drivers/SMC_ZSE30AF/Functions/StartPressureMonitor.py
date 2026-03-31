# DisplayName = Start Pressure Monitoring
# Description = Start Monitoring the sensor to ensure pressure stays within a given range
# Icon = GaugeLowMaterialIcon
# SubIcon = PlayMaterialIcon
# Flags = IsProcessStep, IsTriggerStep, IsHidden

def __inputs__():
    #Optional = True
    #Description = The minimum pressure that must be maintained
    Inputs.Low = new.double(0, -32748, 32747, 0.1, 1, "[Unit]", __source__)

    #Description = The maximum pressure that cannot be exceeded
    Inputs.High = new.double(0, -32748, 32747, 0.1, 1, "[Unit]", __source__)
    
    #DisplayName = Error Immediately
    #Description = A value indicating that the monitor loop should throw an exception as soon as the range is exceeded
    Inputs.ErrorImmediately = new.bool(False)

    #Optional = True
    #DisplayName = Build Pressure Delay
    #Description = The minimum amount of time that must pass before the pressure monitoring begins
    Inputs.BuildPressureDelay = new.int(1000, 0, 5000, 1, 10, "ms")

def __run__():
    if Settings.Analog is None:
        __throwexception__(Exceptions.AnalogInputMissing)
        return

    if not GetIsCalibrated():
        __throwexception__(Exceptions.SensorNotCalibrated)
        return

    deviceParameter = GetDeviceParameter()
    low = float('nan')
    if Inputs.Low is not None:
        low = Inputs.Low.Value

    buildpressuredelay = -1
    if Inputs.BuildPressureDelay is not None:
        buildpressuredelay = Inputs.BuildPressureDelay.Value

    if Inputs.ErrorImmediately.Value:
        PVA.Sensors.StartAnalogSensorMonitoring(deviceParameter, Settings.Output, low, Inputs.High.Value, buildpressuredelay, StopPressureMonitor.Target)
    else:
        PVA.Sensors.StartAnalogSensorMonitoring(deviceParameter, Settings.Output, low, Inputs.High.Value, buildpressuredelay, None)

def __virtual__():
    pass

def __outputs__():
    pass

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
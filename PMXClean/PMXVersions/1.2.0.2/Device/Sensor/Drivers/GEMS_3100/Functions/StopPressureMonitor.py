#DisplayName = Stop Pressure Monitoring
#Description = Stop Monitoring the sensor and throw any errors that were not thrown immediately
#Icon = GaugeLowMaterialIcon
#SubIcon = StopMaterialIcon
#Flags = IsProcessStep, IsTriggerStep, IsHidden

def __inputs__():
    pass

def __run__():
    error = PVA.Sensors.StopAnalogSensorMonitoring(GetDeviceParameter())
    if error is not None:
        if hasattr(error, "High"):
            Exceptions.PressureHigh.ExceptionData.MessageParams = tuple([GetDisplayName(), error.Measurement, error.High, GetMeasurementUnits()])
            PVA.Exceptions.ThrowExceptionAsync(Exceptions.PressureHigh)
        else:
            Exceptions.PressureLow.ExceptionData.MessageParams = tuple([GetDisplayName(), error.Measurement, error.Low, GetMeasurementUnits()])
            PVA.Exceptions.ThrowExceptionAsync(Exceptions.PressureLow)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.PressureLow = new.exception("#Sensor.PressureOutOfRange", "#Sensor.PressureTooLow: {0}\r\n#Sensor.Measurement: {1:N2}{3}\r\n#UI.Minimum: {2:N2}{3}", new.enum("Severity", "Error").Value, None)
    Exceptions.PressureHigh = new.exception("#Sensor.PressureOutOfRange", "#Sensor.PressureTooHigh: {0}\r\n#Sensor.Measurement: {1:N2}{3}\r\n#UI.Maximum: {2:N2}{3}", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
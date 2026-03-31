#DisplayName = Get Reading
#Description = Get a single reading from the width sensor
#Icon = RulerMaterialIcon

def __inputs__():
    pass

def __run__():
    if Settings.Analog is None:
        __throwexception__(Exceptions.AnalogInputMissing)
        return

    if not GetIsCalibrated():
        __throwexception__(Exceptions.SensorNotCalibrated)
        return

    Outputs.Reading.Units = GetMeasurementUnits()
    Outputs.Reading.Value = PollReading().Reading.Value

def __virtual__():
    pass

def __outputs__():
    #Description = The single reading from the sensor
    Outputs.Reading = new.double()

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
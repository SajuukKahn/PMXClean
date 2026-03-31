#DisplayName = Poll Pressure Data
#Description = Poll the sensor for a calibrated pressure reading
#Icon = GaugeLowMaterialIcon
#Flags = IsPolling, IsHidden

analogMissingThrown = False
readings = []
total = 0

def __inputs__():
    pass

def __run__():
    global analogMissingThrown
    global readings
    global total

    if Settings.Analog is None:
        if not analogMissingThrown:
            analogMissingThrown = True
            readings = [0.0]
            total = 0
            Outputs.Reading.Units = GetMeasurementUnits()
            Outputs.Reading.Value = 0
            __throwexception__(Exceptions.AnalogInputMissing, 0, 0, 0)
        return
    analogMissingThrown = False

    maxreadings = 100

    reading = GetMeasurementReading(Settings.Analog.Value)
    noise = GetNoiseTolerance();

    if reading == float("inf") or reading == float("nan"):
        reading = 0.0
        readings = [reading]
        total = reading
    elif reading > -noise and reading < noise:
        reading = 0.0
        readings = [reading]
        total = reading
    elif abs(reading - Outputs.Reading.Value) > noise:
        readings = [reading]
        total = reading
    else:
        readings.append(reading)
        total = total + reading
        if len(readings) > maxreadings:
            total = total - readings.pop(0)

    Outputs.Reading.Units = GetMeasurementUnits()
    Outputs.Reading.Value = total / float(len(readings))
    SetFilteredMeasurement(Outputs.Reading.Value)

    if Outputs.Reading.Value >= Settings.CriticalOverPressure.Value:
        __throwexception__(Exceptions.CriticalOverPressureException, Outputs.Reading.Value, Settings.CriticalOverPressure.Value, GetMeasurementUnits())

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #Description = The polled calibrated pressure reading
    Outputs.Reading = new.double(0, 0, 100, 0.1, 1, "[Unit]", __source__)

def __exceptions__():
    Exceptions.AnalogInputMissing = new.exception("#IO.Exceptions.AnalogInputMissingTitle", "#IO.Exceptions.AnalogInputMissing", new.enum("Severity", "Silent").Value, None)
    Exceptions.CriticalOverPressureException = new.exception("#Sensor.Exceptions.CriticalOverPressureTitle", "#Sensor.Exceptions.CriticalOverPressure\r\n#Sensor.ReadingDuringError: {1:N2}{3}\r\n#Sensor.CriticalPressure: {2:N2}{3}", new.enum("Severity", "Critical").Value, None)

def __throwexception__(exception, currentReading, criticalPressure, units):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), currentReading, criticalPressure, units])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
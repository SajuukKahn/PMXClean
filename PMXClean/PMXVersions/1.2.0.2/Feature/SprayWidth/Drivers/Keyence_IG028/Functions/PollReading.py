#DisplayName = Poll Reading
#Description = Poll the reading from the width sensor
#Icon = RulerMaterialIcon
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
            __throwexception__(Exceptions.AnalogInputMissing)
        return
    analogMissingThrown = False

    maxreadings = 100

    reading = GetMeasurementReading(Settings.Analog.Value)

    if reading == float("inf") or reading == float("nan"):
        reading = 0.0
        readings = [reading]
        total = reading
    elif abs(reading - Outputs.Reading.Value) > GetNoiseTolerance():
        readings = [reading]
        total = reading
    else:
        readings.append(reading)
        total = total + reading
        if len(readings) > maxreadings:
            total = total - readings.pop(0)

    Outputs.Reading.Units = GetMeasurementUnits()
    Outputs.Reading.Value = total / float(len(readings))

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #Description = The polled reading from the sensor
    Outputs.Reading = new.double()

def __exceptions__():
    Exceptions.AnalogInputMissing = new.exception("#IO.Exceptions.AnalogInputMissingTitle", "#IO.Exceptions.AnalogInputMissing", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
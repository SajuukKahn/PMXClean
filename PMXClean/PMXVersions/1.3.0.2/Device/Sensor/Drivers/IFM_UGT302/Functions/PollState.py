#DisplayName = Poll State
#Description = Poll the state of the sensor
#Icon = PollMaterialIcon
#Flags = IsPolling, IsHidden

analogMissingThrown = False
analogNotCalibratedThrown = False
readings = []
total = 0
timeStamp = None
lastState = False

maxreadings = 100

# raw fail-safe values
voltageMin = 0.1
voltageMax = 4.9 # assumes Galil AQx,3, but sensor can change to 9.9 with different AQ values
shortMin = 328
shortMax = 32439
failedReadings = 0
failedReadingsToIgnore = 20

def __inputs__():
    pass

def __run__():
    global analogMissingThrown
    global analogNotCalibratedThrown
    global readings
    global total
    global timeStamp
    global lastState
    global failedReadings

    if Settings.Analog is None:
        reading = float("nan")
        readings = []
        total = 0
        Outputs.Reading.Units = ""
        Outputs.Reading.Value = reading
        Outputs.PolledState.Value = True
        Outputs.IsSettled.Value = True
        timeStamp = None
        lastState = True
        if analogMissingThrown:
            return
        analogMissingThrown = True
        __throwexception__(Exceptions.AnalogInputMissing)
        return
    analogMissingThrown = False

    analogValue = Settings.Analog.Value
    reading = GetMeasurementReading(analogValue)

    if not GetIsCalibrated():
        reading = float("nan")
        readings = []
        total = 0
        Outputs.Reading.Units = ""
        Outputs.Reading.Value = reading
        Outputs.PolledState.Value = True
        Outputs.IsSettled.Value = True
        timeStamp = None
        lastState = True
        if analogNotCalibratedThrown:
            return
        analogNotCalibratedThrown = True
        __throwexception__(Exceptions.SensorNotCalibrated)
        return
    analogNotCalibratedThrown = False

    # failsafe for voltage values, adjust logic as needed
    isVoltage = IsAnalogSignalInVolts()
    isVoltageOutOfRange = isVoltage and (analogValue < voltageMin or analogValue > voltageMax)
    isShortOutOfRange = not isVoltage and (analogValue < shortMin or analogValue > shortMax)
    if isVoltageOutOfRange or isShortOutOfRange:
        failedReadings = failedReadings + 1
        if failedReadings >= failedReadingsToIgnore:
            reading = float("nan")
            readings = []
            total = 0
            Outputs.Reading.Units = ""
            Outputs.Reading.Value = reading
            Outputs.PolledState.Value = True
            Outputs.IsSettled.Value = True
            timeStamp = None
            lastState = True
        return
    failedReadings = 0

    noise = GetNoiseTolerance();
    lowrange = GetLowRange();
    highrange = GetHighRange();

    readings.append(reading)
    total = total + reading
    if len(readings) > maxreadings:
        total = total - readings.pop(0)

    inRange = True
    #if lowrange is not None:
    #    inRange = inRange and reading >= lowrange
    if highrange is not None:
        inRange = inRange and reading < highrange

    currentState = not inRange

    if (lastState != currentState):
        timeStamp = PVA.System.GetCurrentTime().Value
        Outputs.IsSettled.Value = False

    Outputs.Reading.Units = GetMeasurementUnits()
    Outputs.Reading.Value = total / float(len(readings))
    SetFilteredMeasurement(Outputs.Reading.Value)

    if (timeStamp is not None):
        if PVA.System.GetCurrentTime().Value > (Settings.DebounceTime.Value + timeStamp):
            Outputs.PolledState.Value = currentState
            Outputs.IsSettled.Value = True
            timeStamp = None

    lastState = currentState

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Polled State
    #Description = A value indicating the polled state of the sensor
    Outputs.PolledState = new.bool(False, True)

    #Property = True
    #Private = True
    #DisplayName = Is Settled
    #Description = A value indicating that the state of the sensor is stable
    Outputs.IsSettled = new.bool(True, True)

    #Property = True
    #Description = The polled calibrated level reading
    Outputs.Reading = new.double(0, 0, 100, 0.1, 1, "[Unit]", __source__)

def __exceptions__():
    Exceptions.AnalogInputMissing = new.exception("#IO.Exceptions.AnalogInputMissingTitle", "#IO.Exceptions.AnalogInputMissing", new.enum("Severity", "Silent").Value, None)
    Exceptions.SensorNotCalibrated = new.exception("#Sensor.Exceptions.SensorNotCalibratedTitle", "#Sensor.Exceptions.SensorNotCalibrated", new.enum("Severity", "Warning").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
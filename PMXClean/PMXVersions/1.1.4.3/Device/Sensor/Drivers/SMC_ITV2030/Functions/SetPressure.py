# DisplayName = Set Pressure
# Description = Set regulator pressure to a calibrated value
# Icon = GaugeLowMaterialIcon

def __inputs__():
    #Description = The pressure to set the regulator to
    Inputs.Pressure = new.double(0, 0, 32767, 0.1, 1, "[Unit]", __source__)

def __run__():
    if (Settings.AnalogOutput is None):
        __throwexception__(Exceptions.AnalogOutputMissing)
        return

    if (Settings.AnalogInput is None):
        __throwexception__(Exceptions.AnalogInputMissing)
        return

    if (not SetPressureInRange(Inputs.Pressure.Value)):
        __throwexception__(Exceptions.SetPressureOutOfRange)
        return

    Settings.AnalogOutput.Set(ToSignal(Inputs.Pressure.Value))

    lastReading = _PollPressureData_.Reading.Value
    PVA.System.Wait(1000)

    while abs(_PollPressureData_.Reading.Value - lastReading) > .02:
        lastReading = _PollPressureData_.Reading.Value
        PVA.System.Wait(500)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AnalogOutputMissing = new.exception("#IO.Exceptions.AnalogOutputMissingTitle", "#IO.Exceptions.AnalogOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.AnalogInputMissing = new.exception("#IO.Exceptions.AnalogInputMissingTitle", "#IO.Exceptions.AnalogInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.SetPressureOutOfRange = new.exception("#Sensor.Exceptions.SetPressureOutOfRangeTitle", "#Sensor.Exceptions.SetPressureOutOfRange", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
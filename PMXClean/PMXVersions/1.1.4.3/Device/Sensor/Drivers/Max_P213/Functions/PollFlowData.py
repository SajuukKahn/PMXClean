# DisplayName = Poll Flow Data
# Description = Poll the sensor for a calibrated flow reading
# Icon = RulerMaterialIcon
# Flags = IsPolling, IsHidden

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown

    if Settings.Encoder is None:
        if thrown:
            return
        thrown = True
        __throwexception__(Exceptions.EncoderMissing)
        return

    if Settings.KFactor.Value == 0:
        if thrown:
            return
        thrown = True
        __throwexception__(Exceptions.KFactorZero)
        return

    thrown = False
    Outputs.Flow.Value = Settings.Encoder.Value / Settings.KFactor.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #Description = The polled calibrated flow reading
    Outputs.Flow = new.double(0.0, 0.0, 300000.0, 0.01, 1.0, "cc.")

def __exceptions__():
    Exceptions.EncoderMissing = new.exception("#IO.Exceptions.EncoderMissingTitle", "#IO.Exceptions.EncoderMissing", new.enum("Severity", "Silent").Value, None)
    Exceptions.KFactorZero = new.exception("#Sensor.Exceptions.KFactorErrorTitle", "#Sensor.Exceptions.KFactorError", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
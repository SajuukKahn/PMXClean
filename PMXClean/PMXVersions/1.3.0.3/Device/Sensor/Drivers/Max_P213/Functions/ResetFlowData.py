#DisplayName = Reset Flow Data
#Description = Reset the flow data from the sensor
#Flags = IsProgramStep
#Icon = LocationClearCustomIcon

def __inputs__():
    pass

def __run__():
    try:
        resetFlowData()
    except:
        return

def __virtual__():
    pass

def resetFlowData():
    if (Settings.Encoder is None):
        __throwexception__(Exceptions.EncoderMissing)
        raise

    Settings.Encoder.Set(0)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.EncoderMissing = new.exception("#IO.Exceptions.EncoderMissingTitle", "#IO.Exceptions.EncoderMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
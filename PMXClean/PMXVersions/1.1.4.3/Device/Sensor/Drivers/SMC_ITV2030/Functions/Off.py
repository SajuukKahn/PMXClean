# DisplayName = Off
# Description = Turn the regulator output off
# Icon = PowerPlugOffMaterialIcon
# Flags = IsTriggerStep

def __inputs__():
    pass

def __run__():
    if (Settings.Analog is None):
        __throwexception__(Exceptions.AnalogOutputMissing)
        return

    Settings.Analog.Value = 0

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AnalogOutputMissing = new.exception("#IO.Exceptions.AnalogOutputMissingTitle", "#IO.Exceptions.AnalogOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
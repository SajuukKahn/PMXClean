#DisplayName = Off
#Description = Turn the vacuum suction off
#Icon = PowerPlugOffMaterialIcon

def __inputs__():
    pass

def __run__():
    if (Settings.VacuumOutput is None):
        __throwexception__(Exceptions.VacuumOutputMissing)
        return

    Settings.VacuumOutput.Set(False)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.VacuumOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
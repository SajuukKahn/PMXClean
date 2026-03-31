#DisplayName = Off
#Description = Turn the Plasma ionizer off
#Icon = PowerPlugOffMaterialIcon

def __inputs__():
    pass

def __run__():
    timeout = 5000
    postDwell = 300

    if (Settings.GeneratorOn is None):
        __throwexception__(Exceptions.GeneratorOnOutputMissing)
        return

    if (Settings.OnOutput is None):
        __throwexception__(Exceptions.OnOutputMissing)
        return

    if (Settings.Fault is None):
        __throwexception__(Exceptions.FaultInputMissing)
        return

    if (Settings.Ready is None):
        __throwexception__(Exceptions.ReadyInputMissing)
        return

    if (Settings.OnInput is None):
        __throwexception__(Exceptions.OnInputMissing)
        return

    Settings.OnOutput.Set(False)

    waitTime = PVA.System.GetCurrentTime().Value + timeout
    while isOn() and (PVA.System.GetCurrentTime().Value < waitTime):
        if isInFault():
            __throwexception__(Exceptions.PlasmaFaultOn)
            return

        PVA.System.Wait(10)

    if isOn():
        __throwexception__(Exceptions.PlasmaOffTimeout)
        return

    # dwell after plasma turned off
    PVA.System.Wait(postDwell)

def isInFault():
    return Settings.Fault.Value == Settings.FaultState.Value

def isOn():
    return Settings.OnInput.Value == Settings.OnState.Value

def __outputs__():
    pass

def __exceptions__():
    Exceptions.GeneratorOnOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Cleaning.Exceptions.PlasmaGeneratorOnOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OnOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Cleaning.Exceptions.PlasmaOnOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.FaultInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Cleaning.Exceptions.PlasmaFaultInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ReadyInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Cleaning.Exceptions.PlasmaReadyInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OnInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Cleaning.Exceptions.PlasmaOnInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.PlasmaFaultOn = new.exception("#Cleaning.Exceptions.PlasmaErrorTitle", "#Cleaning.Exceptions.PlasmaFaultOn", new.enum("Severity", "Error").Value, None)
    Exceptions.PlasmaOffTimeout = new.exception("#Cleaning.Exceptions.PlasmaErrorTitle", "#Cleaning.Exceptions.PlasmaOffTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.PlasmaReadyTimeout = new.exception("#Cleaning.Exceptions.PlasmaErrorTitle", "#Cleaning.Exceptions.PlasmaReadyTimeout", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
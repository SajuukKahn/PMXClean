#DisplayName = Generator Reset
#Description = Reset the plasma generator
#Icon = RestartMaterialIcon
#Flags = IsTriggerStep

def __inputs__():
    pass

def __run__():
    if (Settings.FaultReset is None) and (Settings.ControlRelay is None):
        __throwexception__(Exceptions.FaultResetOrControlRelayMissing)
        return

    if (Settings.GeneratorOn is None):
        __throwexception__(Exceptions.GeneratorOnOutputMissing)
        return

    if (Settings.Fault is None):
        __throwexception__(Exceptions.FaultInputMissing)
        return

    if (Settings.Ready is None):
        __throwexception__(Exceptions.ReadyInputMissing)
        return

    if Settings.ControlRelay is not None:
        Settings.ControlRelay.Set(True)

    if Settings.FaultReset is not None:
        Settings.FaultReset.Set(True)

        timeout = PVA.System.GetCurrentTime().Value + 5000
        while isInFault() and (PVA.System.GetCurrentTime().Value < timeout):
            PVA.System.Wait(10)
            Settings.FaultReset.Set(True)

        Settings.FaultReset.Set(False)

    if isInFault():
        __throwexception__(Exceptions.PlasmaFaultOn)
        return

    if not isReady():
        Settings.GeneratorOn.Set(True)

        timeout = PVA.System.GetCurrentTime().Value + 5000
        while (not isReady()) and (PVA.System.GetCurrentTime().Value < timeout):
            if isInFault():
                __throwexception__(Exceptions.PlasmaFaultOn)
                return

            PVA.System.Wait(10)

        if not isReady():
            __throwexception__(Exceptions.PlasmaError)
            return

def isInFault():
    return Settings.Fault.Value == Settings.FaultState.Value

def isReady():
    return Settings.Ready.Value == Settings.ReadyState.Value

def __outputs__():
    pass

def __exceptions__():
    Exceptions.FaultResetOrControlRelayMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Cleaning.Exceptions.PlasmaGeneratorOnOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.GeneratorOnOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Cleaning.Exceptions.PlasmaGeneratorOnOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.FaultInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Cleaning.Exceptions.PlasmaFaultInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ReadyInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Cleaning.Exceptions.PlasmaReadyInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OnInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Cleaning.Exceptions.PlasmaOnInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.PlasmaFaultOn = new.exception("#Cleaning.Exceptions.PlasmaErrorTitle", "#Cleaning.Exceptions.PlasmaFaultOn", new.enum("Severity", "Error").Value, None)
    Exceptions.PlasmaError = new.exception("#Cleaning.Exceptions.PlasmaErrorTitle", "#Cleaning.Exceptions.PlasmaError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
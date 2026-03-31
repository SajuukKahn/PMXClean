#DisplayName = Poll Error
#Description = Error checking for the plasma head
#Icon = SignCautionMaterialIcon
#Flags = IsHidden, IsPolling

timeoutoff = -1

def __inputs__():
    pass

def __run__():
    global timeoutoff
    timeout = 5000

    if (Settings.Fault is None) or (Settings.OnOutput is None) or (Settings.Ready is None):
        return

    if (isReady() and not isOn()) or (timeoutoff == -1):
        timeoutoff = PVA.System.GetCurrentTime().Value + timeout

    if (not isReady() and isOn() and (PVA.System.GetCurrentTime().Value < timeoutoff)):
        __throwexception__(Exceptions.PlasmaError)

def isInFault():
    return Settings.Fault.Value == Settings.FaultState.Value

def isReady():
    return Settings.Ready.Value == Settings.ReadyState.Value

def isOn():
    return Settings.OnInput.Value == Settings.OnState.Value

def __outputs__():
    pass

def __exceptions__():
    Exceptions.PlasmaError = new.exception("#Cleaning.Exceptions.PlasmaErrorTitle", "#Cleaning.Exceptions.PlasmaError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
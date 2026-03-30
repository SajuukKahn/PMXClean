#DisplayName = Off
#Description = Turn the SJ100 off
#Icon = PowerPlugOffMaterialIcon

def __inputs__():
    #Description = A value indicating whether to hault immediately and ignore remaining cycles
    Inputs.Halt = new.bool(False)

def __run__():
    if Settings.Trigger is None:
        __throwexception__(Exceptions.TriggerOutputMissing)
        return

    Settings.Trigger.Set(False)

    if Inputs.Halt.Value and not Settings.Ready.Value:
        SendPacket(Settings.Header.Value + "X")

def __outputs__():
    pass

def __exceptions__():
    Exceptions.TriggerOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Valve.Exceptions.TriggerOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
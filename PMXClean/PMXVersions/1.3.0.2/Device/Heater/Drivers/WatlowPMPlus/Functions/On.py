#DisplayName = On
#Description = Turn the heater on
#Icon = PowerPlugMaterialIcon
#SubIcon = FireMaterialIcon
#Flags = IsQuickAction, IsTriggerStep, IsProcessStep

def __inputs__():
    pass

def __run__():
    if (not GetIsOn()):
        if (Settings.HeaterOnOutput is None):
            SendPacket(BuildModbusPacket(16, 1880, 10))
        else:
            Settings.HeaterOnOutput.Set(True)
        SetIsOn(True)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.HeaterOnOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Heater.Exceptions.HeaterOnOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
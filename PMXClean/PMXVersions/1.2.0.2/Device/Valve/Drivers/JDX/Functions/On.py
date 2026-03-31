#DisplayName = On
#Description = Turn the JDX on
#Icon = PowerPlugMaterialIcon

def __inputs__():
    pass

def __run__():
    if Settings.Ready is None:
        __throwexception__(Exceptions.ReadyInputMissing)
        return

    if Settings.Trigger is None:
        __throwexception__(Exceptions.TriggerOutputMissing)
        return

    if Settings.Ready.Value == False:
        Off(new.bool(True))
        __throwexception__(Exceptions.NotReady)
        return

    Settings.Trigger.Set(True)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ReadyInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Valve.Exceptions.ReadyInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.TriggerOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Valve.Exceptions.TriggerOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.NotReady = new.exception("#Valve.Exceptions.JDXExceptionTitle", "#Valve.Exceptions.NotReady", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
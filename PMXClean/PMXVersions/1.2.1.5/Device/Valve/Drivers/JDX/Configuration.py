def __settings__():
    #Reserved = True
    Settings.Trigger = new.output()

    #Reserved = true
    Settings.Ready = new.input()

    Settings.Header = new.string("\u0002")
    Settings.Footer = new.string("\u0003")

def onconnect():
    SendPacket(Settings.Header.Value + "$VA000000000000" + Settings.Footer.Value)

def ready():
    if (Settings.Ready is None):
        __throwexception__(Exceptions.ReadyOutputMissing)
        return

    if (Settings.Trigger is None):
        __throwexception__(Exceptions.TriggerOutputMissing)
        return

def complete():
    ready = Settings.Ready.Value
    timeout = PVA.System.GetCurrentTime().Value + 4000
    while (ready is False) and (PVA.System.GetCurrentTime().Value < timeout):
        PVA.System.Wait(10)
        ready = Settings.Ready.Value

def __exceptions__():
    Exceptions.ReadyInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Valve.Exceptions.ReadyInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.TriggerOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Valve.Exceptions.TriggerOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
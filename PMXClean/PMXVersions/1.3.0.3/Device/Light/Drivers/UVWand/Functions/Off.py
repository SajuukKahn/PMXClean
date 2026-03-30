#DisplayName = Off
#Description = Turn the UV Wand off
#Icon = LedOffMaterialIcon

def __inputs__():
    pass

def __run__():
    if (Settings.Output is None):
        __throwexception__(Exceptions.OutputMissing)
        return

    if (Settings.ShutterInput is None):
        __throwexception__(Exceptions.ShutterInputMissing)
        return

    # Delay for quickly toggling UV wand shutter
    PVA.System.Wait(250)

    if Settings.HandshakeOption.Value == "Latching":
        Settings.Output.Set(False)
    elif Settings.HandshakeOption.Value == "Toggle":
        Settings.Output.Set(True)
        PVA.System.Wait(100)
        Settings.Output.Set(False)

    # Check to make sure shutter closes
    closed = isshutterclosed()
    timeout = PVA.System.GetCurrentTime().Value + 2000
    while (closed is False) and (PVA.System.GetCurrentTime().Value < timeout):
        PVA.System.Wait(50)
        closed = isshutterclosed()

    if closed is False:
        __throwexception__(Exceptions.ShutterCloseFailed)
        return

def __virtual__():
    pass

def __outputs__():
    pass

def isshutterclosed():
    return Settings.ShutterInput.Value != Settings.ShutterOpenState.Value

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ShutterInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Light.Exceptions.ShutterInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ShutterCloseFailed = new.exception("#Light.Exceptions.UVExceptionTitle", "#Light.Exceptions.ShutterCloseFailed", new.enum("Severity", "Error").Value, None)

def __releaseresources__():
    PVA.Safety.ResetBypassOK()

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
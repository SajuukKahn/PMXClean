#DisplayName = On
#Description = Turn the UV Wand on
#Icon = LedOnMaterialIcon

def __inputs__():
    pass

def __run__():
    if (Settings.Output is None):
        __throwexception__(Exceptions.OutputMissing)
        return

    if (Settings.OnInput is None):
        __throwexception__(Exceptions.OnInputMissing)
        return

    if (Settings.ShutterInput is None):
        __throwexception__(Exceptions.ShutterInputMissing)
        return

    if (Settings.OnInput.Value == False):
        __throwexception__(Exceptions.LightNotOn)
        return

    # Delay for quickly toggling UV wand shutter
    PVA.System.Wait(250)

    Settings.Output.Set(True)

    # Check to make sure shutter opens
    opened = isshutteropen()
    timeout = PVA.System.GetCurrentTime().Value + 2000
    while (opened is False) and (PVA.System.GetCurrentTime().Value < timeout):
        PVA.System.Wait(50)
        opened = isshutteropen()

    if opened is False:
        __throwexception__(Exceptions.ShutterOpenFailed)
        return

def __virtual__():
    pass

def __outputs__():
    pass

def isshutteropen():
    return Settings.ShutterInput.Value == Settings.ShutterOpenState.Value

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OnInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Light.Exceptions.OnInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ShutterInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Light.Exceptions.ShutterInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.LightNotOn = new.exception("#Light.Exceptions.UVExceptionTitle", "#Light.Exceptions.LightNotOn", new.enum("Severity", "Error").Value, None)
    Exceptions.DoorOpen = new.exception("#Light.Exceptions.UVExceptionTitle", "#Light.Exceptions.DoorOpen", new.enum("Severity", "Error").Value, None)
    Exceptions.ShutterOpenFailed = new.exception("#Light.Exceptions.UVExceptionTitle", "#Light.Exceptions.ShutterOpenFailed", new.enum("Severity", "Error").Value, None)

def __lockresources__():
    PVA.Safety.SetBypassOK(False)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    PVA.Safety.ResetBypassOK()

def __exceptionrecovery__():
    pass
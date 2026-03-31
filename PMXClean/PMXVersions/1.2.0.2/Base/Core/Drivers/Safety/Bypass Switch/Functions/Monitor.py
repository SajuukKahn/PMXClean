#DisplayName = Bypass Switch Monitor
#Description = Monitor the bypass switch status.
#Icon = MonitorEyeMaterialIcon
#Flags = IsHidden

wasBypassOn = False
isInError = False
dialogName = "monitorBypass"

def __inputs__():
    pass

def __run__():
    global wasBypassOn
    global isInError

    if Settings.Input is None:
        __throwexception__(Exceptions.InputMissing)
        return

    bypassOK = PVA.Safety.GetDoorBypassOK()

    if isBypassOn() is True:
        if bypassOK is False:
            doorClosed = PVA.Safety.GetDoorClosed()
            if not doorClosed:
                return
            if wasBypassOn:
                waitBypassOff()
            else:
                isInError = True
                wasBypassOn = True
                Outputs.BypassOn.Value = False
                __throwexception__(Exceptions.BypassError)
    if not isInError:
        wasBypassOn = isBypassOn()
        Outputs.BypassOn.Value = wasBypassOn

def __virtual__():
    pass

def isBypassOn():
    return Settings.Input.Value == Settings.BypassState.Value

def waitBypassOff():
    global dialogName
    global isInError
    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, GetDisplayName() + " #Safety.On")
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.TurnOff " + GetDisplayName() + " #Safety.ToContinue")
    PVA.Messaging.SetDialogIcon(dialogName, "ElectricSwitchMaterialIcon")
    PVA.Messaging.ShowDialogAsync(dialogName)

    while isBypassOn():
        PVA.System.Wait(25)

    PVA.Messaging.CloseDialog(dialogName)
    isInError = False

def __outputs__():
    #Property = True
    #DisplayName = Bypass On
    #Description = Value indicating that the bypass is in the on state.
    Outputs.BypassOn = new.bool(False)

def __exceptions__():
    Exceptions.BypassError = new.exception("#Safety.Exceptions.BypassOnTitle", "#Safety.Exceptions.BypassOn", new.enum("Severity", "Critical").Value, __exceptionmessaging__, False, new.device("Andon Light", 0), [1, 0, 0, 0])
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionmessaging__():
    global dialogName
    global isInError
    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.TurnOff " + GetDisplayName())
    PVA.Messaging.SetDialogTitle(dialogName, GetDisplayName() + " #Safety.On")
    PVA.Messaging.SetDialogIcon(dialogName, "ElectricSwitchMaterialIcon")
    PVA.Messaging.SetShutdownButtonIsEnabled(dialogName, True)
    PVA.Messaging.SetShutdownButtonIsVisible(dialogName, True)
    PVA.Messaging.ShowDialogAsync(dialogName)
    waitRecover()

    PVA.Messaging.CloseDialog(dialogName)
    isInError = False

def waitRecover():
    while isBypassOn():
        PVA.System.Wait(25)

def __exceptionrecovery__():
    pass
#DisplayName = Hardware Setup
#Description = Keep the JDX solenoid actuated until turned off
#Icon = CogMaterialIcon
#Flags = IsQuickAction

dialogName = "JDX_Hardware_Setup"
cancel = False

def __inputs__():
    pass

def __run__():
    global dialogName
    global cancel
    displayName = GetDisplayName()
    jetPressureMin = "40 psi"
    cancel = False

    if Settings.Ready is None:
        __throwexception__(Exceptions.ReadyInputMissing)
        return

    if Settings.Trigger is None:
        __throwexception__(Exceptions.TriggerOutputMissing)
        return

    Settings.Trigger.Set(False)

    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, "#Valve.JDX.SetupTitle")
    PVA.Messaging.SetDialogIcon(dialogName, "CogMaterialIcon")
    PVA.Messaging.SetDialogMessageWithParameters(dialogName, "#Valve.JDX.EnsurePressure", jetPressureMin)
    PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#UI.Cancel", setcancel)
    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#UI.Continue", None)
    PVA.Messaging.ShowDialogAsync(dialogName)

    while not PVA.Messaging.CheckDialogInteraction(dialogName):
        PVA.System.Wait(25)

    # here to catch cancel being set
    PVA.System.Wait(250)

    if cancel:
        return

    SendPacket(Settings.Header.Value + "00100,00100,999" + Settings.Footer.Value)

    PVA.System.Wait(90)

    ready = Settings.Ready.Value
    timeout = PVA.System.GetCurrentTime().Value + 2000
    while (ready is False) and (PVA.System.GetCurrentTime().Value < timeout):
        PVA.System.Wait(10)
        ready = Settings.Ready.Value

    if ready is False:
        __throwexception__(Exceptions.JDXTimeout)
        return

    Settings.Trigger.Set(True)

    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, "#Valve.JDX.SetupTitle")
    PVA.Messaging.SetDialogIcon(dialogName, "CogMaterialIcon")
    PVA.Messaging.SetDialogMessageWithParameters(dialogName, "#Valve.JDX.AcknowledgeCompletion", displayName)
    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#UI.Complete", None)
    PVA.Messaging.ShowDialogAsync(dialogName)

    while not PVA.Messaging.CheckDialogInteraction(dialogName):
        PVA.System.Wait(25)

    Settings.Trigger.Set(False)

    PVA.System.Wait(90)
    # some default state
    SetParameters(new.int(10), new.int(10), new.int(10), new.bool(False))

def __virtual__():
    pass

def setcancel():
    global cancel
    cancel = True

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ReadyInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#Valve.Exceptions.ReadyInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.TriggerOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Valve.Exceptions.TriggerOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.JDXTimeout = new.exception("#Valve.Exceptions.JDXExceptionTitle", "#Valve.Exceptions.JDXTimeout", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
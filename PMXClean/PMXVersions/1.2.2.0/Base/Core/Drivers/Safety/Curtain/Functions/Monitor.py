#DisplayName = Curtain Monitor
#Description = Monitor the curtain status
#Icon = MonitorEyeMaterialIcon
#Flags = IsHidden

dialogName = "monitorCurtain"

def __inputs__():
    pass

def __run__():
    if Settings.Input is None:
        __throwexception__(Exceptions.InputMissing)
        return

    curtainClear = PVA.Safety.GetBypassedInterlockDevicesOK()
    processInterlockBlock = PVA.Safety.GetProcessSafetyInterlockBlock()
    curtainBypassOK = PVA.Safety.GetSafetyInterlockBypassOK()
    isBypassOn = PVA.Safety.IsSafetyInterlockBypassOn()
    stopState = inStopState()

    if stopState is True:
        if isBypassOn is True:
            if curtainBypassOK is False:
                if curtainClear is False:
                    waitCurtainClear()
                    PVA.Safety.SetBypassedInterlockDevicesOK(True)
                else:
                    Outputs.Clear.Value = False
                    __throwexception__(Exceptions.StopStateActivated)
            else:
                PVA.Safety.SetBypassedInterlockDevicesOK(False)
        elif processInterlockBlock is True:
            PVA.Safety.SetBypassedInterlockDevicesOK(False)
        else:
            Outputs.Clear.Value = False
            __stopMotors__()
            __throwexception__(Exceptions.StopStateActivated)
    else:
        PVA.Safety.SetBypassedInterlockDevicesOK(True)

    Outputs.Clear.Value = PVA.Safety.GetBypassedInterlockDevicesOK()

def __virtual__():
    pass

def inStopState():
    return (Settings.Input.Value == Settings.StopState.Value)

def waitCurtainClear():
    global dialogName
    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, GetDisplayName() + " #Safety.Break")
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.Clear " + GetDisplayName() + " #Safety.ToContinue")
    PVA.Messaging.SetDialogIcon(dialogName, "LightCurtainClearCustomIcon")
    PVA.Messaging.ShowDialogAsync(dialogName)

    while inStopState():
        if PVA.Safety.IsSafetyInterlockBypassOn() is False:
            PVA.Messaging.CloseDialog(dialogName)
            Outputs.Clear.Value = False
            __throwexception__(Exceptions.StopStateActivated)
        PVA.System.Wait(25)

    PVA.Messaging.CloseDialog(dialogName)

def __outputs__():
    #Property = True
    #Description = Value indicating that the curtain is in the clear state.
    Outputs.Clear = new.bool(True)

def __exceptions__():
    Exceptions.StopStateActivated = new.exception("#Safety.Exceptions.CurtainOpenTitle", "#Safety.Exceptions.CurtainOpen", new.enum("Severity", "Critical").Value, __exceptionmessaging__, False, new.device("Andon Light", 0), [1, 0, 0, 0])
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)

def __exceptionmessaging__():
    global dialogName
    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.Clear " + GetDisplayName())
    PVA.Messaging.SetDialogTitle(dialogName, GetDisplayName() + " #Safety.Clear")
    PVA.Messaging.SetDialogIcon(dialogName, "LightCurtainClearCustomIcon")
    PVA.Messaging.SetShutdownButtonIsEnabled(dialogName, True)
    PVA.Messaging.SetShutdownButtonIsVisible(dialogName, True)
    PVA.Messaging.ShowDialogAsync(dialogName)
    waitRecover()

    PVA.Messaging.CloseDialog(dialogName)

def waitRecover():   
    while inStopState():
        PVA.System.Wait(25)

def __exceptionrecovery__():
    pass

def __stopMotors__():
    for keyValuePair in PVA.Controllers:
        if hasattr(keyValuePair.Value, "MotorOff"):
            controller = keyValuePair.Value
            controller.MotorOff()
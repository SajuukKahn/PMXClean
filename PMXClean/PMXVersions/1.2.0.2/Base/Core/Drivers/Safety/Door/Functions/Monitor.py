#DisplayName = Door Monitor
#Description = Monitor the door status.
#Icon = MonitorEyeMaterialIcon
#Flags = IsHidden

dialogName = "monitorDoor"

def __inputs__():
    pass

def __run__():
    if Settings.Input is None:
        __throwexception__(Exceptions.InputMissing)
        return

    doorClosed = PVA.Safety.GetDoorClosed()
    processDoorBlock = PVA.Safety.GetProcessDoorBlock()
    doorBypassOK = PVA.Safety.GetDoorBypassOK()
    isBypassOn = PVA.Safety.IsDoorBypassDeviceOn()
    stopState = inStopState()

    if stopState is True:
        if isBypassOn is True:
            if doorBypassOK is False:
                if doorClosed is False:
                    waitDoorClose()
                    PVA.Safety.SetDoorClosed(True)
                else:
                    Outputs.Closed.Value = False
                    __throwexception__(Exceptions.StopStateActivated)
            else:
                PVA.Safety.SetDoorClosed(False)
        elif processDoorBlock is True:
            PVA.Safety.SetDoorClosed(False)
        else:
            Outputs.Closed.Value = False
            __throwexception__(Exceptions.StopStateActivated)
    else:
        PVA.Safety.SetDoorClosed(True)

    Outputs.Closed.Value = PVA.Safety.GetDoorClosed()

def __virtual__():
    pass

def inStopState():
    return (Settings.Input.Value == Settings.StopState.Value)

def waitDoorClose():
    global dialogName
    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, GetDisplayName() + " #Safety.Open")
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.Close " + GetDisplayName() + " #Safety.ToContinue")
    PVA.Messaging.SetDialogIcon(dialogName, "DoorSlidingMaterialIcon")
    PVA.Messaging.ShowDialogAsync(dialogName)

    while inStopState():
        if PVA.Safety.IsDoorBypassDeviceOn() is False:
            PVA.Messaging.CloseDialog(dialogName)
            Outputs.Closed.Value = False
            __throwexception__(Exceptions.StopStateActivated)
        PVA.System.Wait(25)

    PVA.Messaging.CloseDialog(dialogName)

def __outputs__():
    #Property = True
    #Description = Value indicating that the door is in the closed state.
    Outputs.Closed = new.bool(True)

def __exceptions__():
    Exceptions.StopStateActivated = new.exception("#Safety.Exceptions.DoorOpenTitle", "#Safety.Exceptions.DoorOpen", new.enum("Severity", "Critical").Value, __exceptionmessaging__, False, new.device("Andon Light", 0), [1, 0, 0, 0])
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
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.Close " + GetDisplayName())
    PVA.Messaging.SetDialogTitle(dialogName, GetDisplayName() + " #Safety.Open")
    PVA.Messaging.SetDialogIcon(dialogName, "DoorSlidingMaterialIcon")
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
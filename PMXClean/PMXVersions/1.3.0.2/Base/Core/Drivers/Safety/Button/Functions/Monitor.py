#DisplayName = Button Monitor
#Description = Monitor the button status
#Icon = MonitorEyeMaterialIcon
#Flags = IsHidden

dialogName = "monitorButton"

def __inputs__():
    pass

def __run__():
    if Settings.Input is None:
        __throwexception__(Exceptions.InputMissing)
        return

    if (Settings.Input.Value == Settings.StopState.Value):
        Outputs.IsPressed.Value = True
        __stopMotors__()
        __throwexception__(Exceptions.StopStateActivated)
    else:
        Outputs.IsPressed.Value = False

def __virtual__():
    pass

def inStopState():
    return (Settings.Input.Value == Settings.StopState.Value)

def __outputs__():
    #Property = True
    #DisplayName = Is Pressed
    #Description = Value indicating that the button is pressed
    Outputs.IsPressed = new.bool(False, True)

def __exceptions__():
    Exceptions.StopStateActivated = new.exception("#Safety.Exceptions.ButtonPressedTitle", "#Safety.Exceptions.ButtonPressed", new.enum("Severity", "Critical").Value, __exceptionmessaging__, False, new.device("Andon Light", 0), [1, 0, 0, 0])
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionmessaging__():
    global dialogName
    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.Release " + GetDisplayName())
    PVA.Messaging.SetDialogTitle(dialogName, GetDisplayName() + " #Safety.Pressed")
    PVA.Messaging.SetDialogIcon(dialogName, "GestureUnTapButtonMaterialIcon")
    PVA.Messaging.SetShutdownButtonIsEnabled(dialogName, True)
    PVA.Messaging.SetShutdownButtonIsVisible(dialogName, True)
    PVA.Messaging.SetDialogHighPriority(dialogName, True)
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
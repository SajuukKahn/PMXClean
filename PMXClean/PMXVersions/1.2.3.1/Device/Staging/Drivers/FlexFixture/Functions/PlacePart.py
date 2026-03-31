#DisplayName = Place Part
#Description = Part handling routine that allows the use of the interlock bypass to manually load parts, and then awaits the cycle start input to continue execution flow
#Icon = DownloadOutlineMaterialIcon
#Flags = IsProcessStep, IsHidden

dialogName = "PlacePart"
canceled = False
confirmed = False
robotReserved = False

def __inputs__():
    #DisplayName = Bypass Part Check
    #Description = A value indicating whether to skip checking the input for part presence
    Inputs.BypassPartCheck = new.bool(True)

    #DisplayName = Require Confirmation
    #Description = A value indicating whether to have the user acknowledge that the part is in place before continuing
    Inputs.RequireConfirmation = new.bool(False)

    #Description = The robot to reserve 
    Inputs.Robot = new.robot("Controller0", 0)

def __run__():
    global dialogName
    global canceled
    global confirmed
    canceled = False
    confirmed = False
    if Settings.CycleStart is None:
        __throwexception__(Exceptions.NoInput, "Cycle Start Input")

    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, "#Staging.PlacePart")
    PVA.Messaging.SetDialogIcon(dialogName, "DownloadOutlineMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Blue")
    PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#Process.AbortProcess", __cancelExecution__)
    PVA.Messaging.ShowDialogAsync(dialogName)

    partPlaced = IsPartPlaced.Value
    startPressed = False
    if not partPlaced:
        stopMotors()
        PVA.System.Wait(250)
        PVA.Safety.SetControlPowerOff()
        PVA.Safety.SetProcessSafetyInterlockBlock(True)
        PVA.Safety.SetBypassOK(True)

        wasInterlockOpened = False
        partPlaced = Inputs.BypassPartCheck.Value or Settings.PartSensor is None or Settings.PartSensor.CheckState().State.Value
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.PlacePartPrompt")
        while not confirmed:
            if canceled:
                onCancel()
                return
            wasInterlockOpened = wasInterlockOpened or not PVA.Safety.GetBypassedInterlockDevicesOK()
            isInterlockClosed = wasInterlockOpened and PVA.Safety.GetBypassedInterlockDevicesOK()
            partPlaced = Inputs.BypassPartCheck.Value or Settings.PartSensor is None or Settings.PartSensor.CheckState().State.Value
            if wasInterlockOpened and isInterlockClosed and partPlaced:
                if Inputs.RequireConfirmation.Value:
                    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.PressOKToContinue")
                    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#Messaging.OK", confirm)
                else:
                    confirmed = True

                if Settings.CycleStart.Value == Settings.CycleStartOnState.Value:
                    startPressed = True
                    confirmed = True
            else:
                PVA.Messaging.SetDialogMessage(dialogName, "#Staging.PlacePartPrompt")
                PVA.Messaging.SetDialogButtonProperties(dialogName, 3, False, False, False, "#Messaging.OK", None)
            PVA.System.Wait(10)

        PVA.Messaging.SetDialogButtonProperties(dialogName, 3, False, False, False, "#Messaging.OK", None)
        PVA.Safety.ForceClosedState()
        PVA.Safety.ResetBypassOK()
        PVA.Safety.SetProcessSafetyInterlockBlock(False)
        PVA.Safety.SetControlPowerOn()
        PVA.System.Wait(250)
        __servoMotors__()
        __releaseresources__()

        IsPartPlaced.Value = True

    if not startPressed:
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.PressCycleStart")
        while not startPressed:
            if canceled:
                onCancel()
                return
            startPressed = Settings.CycleStart.Value == Settings.CycleStartOnState.Value
            PVA.System.Wait(10)
    
    PVA.Messaging.SetDialogButtonProperties(dialogName, 0, False, False, False, "#UI.Cancel", None)
    PVA.Messaging.CloseDialog(dialogName)

def __virtual__():
    pass

def confirm():
    global confirmed
    confirmed = True

def stopMotors():
    for keyValuePair in PVA.Controllers:
        if hasattr(keyValuePair.Value, "MotorOff"):
            controller = keyValuePair.Value
            controller.MotorOff()

def __servoMotors__():
    for keyValuePair in PVA.Controllers:
        if hasattr(keyValuePair.Value, "ServoAxes"):
            controller = keyValuePair.Value
            controller.ServoAxes()

def onCancel():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)

    PVA.Safety.SetProcessSafetyInterlockBlock(False)
    PVA.Safety.ResetBypassOK()
    PVA.Safety.SetControlPowerOn()
    PVA.System.Wait(250)
    __servoMotors__()
    PVA.Process.CancelExecution()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.NoInput = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Safety.SetProcessSafetyInterlockBlock(False)
    PVA.Safety.ResetBypassOK()
    IsPartPlaced.Value = False

def __exceptionrecovery__():
    pass

def __cancelExecution__():
    global canceled
    global confirmed
    IsPartPlaced.Value = False
    canceled = True
    confirmed = False

def __lockresources__():
    global robotReserved
    if Inputs.Robot is not None:
        Inputs.Robot.RequestMove()
        Inputs.Robot.Reserve()
        robotReserved = True

def __releaseresources__():
    global robotReserved
    if Inputs.Robot is not None and robotReserved:
        Inputs.Robot.Release()
        Inputs.Robot.MoveComplete()
        robotReserved = False
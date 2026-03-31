#DisplayName = Remove Part
#Description = Part handling routine that allows the use of the interlock bypass to manually unload parts, and then awaits the interlock safety input to continue execution flow
#Icon = UploadOutlineMaterialIcon
#Flags = IsProcessStep, IsHidden

dialogName = "RemovePart"
canceled = False
confirmed = False

def __inputs__():
    #DisplayName = Bypass Part Check
    #Description = A value indicating whether to skip checking the input for part presence
    Inputs.BypassPartCheck = new.bool(False)

    #DisplayName = Place While Removing
    #Description = A value indicating whether to prompt the user to place a new part while removing the old part
    Inputs.PlaceWhileRemoving = new.bool(True)

    #DisplayName = Require Confirmation
    #Description = A value indicating whether to have the user acknowledge that the part is in place or removed before continuing
    Inputs.RequireConfirmation = new.bool(False)

    #Description = The robot to reserve 
    Inputs.Robot = new.robot("Controller0", 0)

def __run__():
    global dialogName
    global canceled
    global confirmed
    canceled = False
    confirmed = False

    stopMotors()
    PVA.System.Wait(250)
    PVA.Safety.SetControlPowerOff()
    PVA.Safety.SetProcessSafetyInterlockBlock(True)
    PVA.Safety.SetBypassOK(True)
    if not Settings.PartSensor is None:
        partPlaced = Settings.PartSensor.CheckState().State.Value
    else:
        partPlaced = False

    PVA.Messaging.CreateDialog(dialogName)
    if Inputs.PlaceWhileRemoving.Value:
        PVA.Messaging.SetDialogTitle(dialogName, "#Staging.ReplacePart")
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.ReplacePartPrompt")
    else:
        PVA.Messaging.SetDialogTitle(dialogName, "#Staging.RemovePart")
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.RemovePartPrompt")
    PVA.Messaging.SetDialogIcon(dialogName, "UploadOutlineMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Blue")
    PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#Process.AbortProcess", __cancelExecution__)
    PVA.Messaging.ShowDialogAsync(dialogName)

    wasInterlockOpened = False
    while not confirmed:
        if canceled:
            onCancel()
            return
        wasInterlockOpened = wasInterlockOpened or not PVA.Safety.GetBypassedInterlockDevicesOK()
        isInterlockClosed = wasInterlockOpened and PVA.Safety.GetBypassedInterlockDevicesOK()
        partRemoved = Inputs.BypassPartCheck.Value or Settings.PartSensor is None or not Settings.PartSensor.CheckState().State.Value
        partReplaced = partRemoved and (Inputs.BypassPartCheck.Value or Settings.PartSensor is None or Settings.PartSensor.CheckState().State.Value)
        if wasInterlockOpened and isInterlockClosed and partRemoved and (partReplaced or not Inputs.PlaceWhileRemoving.Value):
            if Inputs.RequireConfirmation.Value:
                PVA.Messaging.SetDialogMessage(dialogName, "#Safety.PressOKToContinue")
                PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#Messaging.OK", confirm)
            else:
                confirmed = True
        else:
            if Inputs.PlaceWhileRemoving.Value:
                PVA.Messaging.SetDialogTitle(dialogName, "#Staging.ReplacePart")
                PVA.Messaging.SetDialogMessage(dialogName, "#Staging.ReplacePartPrompt")
            else:
                PVA.Messaging.SetDialogTitle(dialogName, "#Staging.RemovePart")
                PVA.Messaging.SetDialogMessage(dialogName, "#Staging.RemovePartPrompt")
            PVA.Messaging.SetDialogButtonProperties(dialogName, 3, False, False, False, "#Messaging.OK", None)
        PVA.System.Wait(10)
        
    PVA.Safety.ForceClosedState()
    PVA.Safety.ResetBypassOK()
    PVA.Safety.SetProcessSafetyInterlockBlock(False)
    PVA.Safety.SetControlPowerOn()
    PVA.System.Wait(250)
    __servoMotors__()

    if not Inputs.PlaceWhileRemoving.Value:
        IsPartPlaced.Value = False

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
    pass

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
    IsPartPlaced.Value = False
    canceled = True

def __lockresources__():
    if Inputs.Robot is not None:
        Inputs.Robot.RequestMove()
        Inputs.Robot.Reserve()

def __releaseresources__():
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
        Inputs.Robot.MoveComplete()
#DisplayName = Remove Part
#Description = Part handling routine that allows the use of the door bypass to manually unload parts, and then awaits the door safety input to continue execution flow
#Icon = UploadOutlineMaterialIcon
#Flags = IsProcessStep, IsHidden

dialogName = "RemovePart"
canceled = False

def __inputs__():
    #DisplayName = Bypass Part Check
    #Description = A value indicating whether to skip checking for part presence
    Inputs.BypassPartCheck = new.bool(False)

    #DisplayName = Place While Removing
    #Description = A value indicating whether to prompt the user to place a new part while removing the old part
    Inputs.PlaceWhileRemoving = new.bool(True)

def __run__():
    global dialogName
    global canceled
    canceled = False

    stopMotors()
    PVA.System.Wait(250)
    PVA.Safety.SetControlPowerOff()
    PVA.Safety.SetProcessDoorBlock(True)
    PVA.Safety.SetDoorBypassOK(True)
    if not Settings.PartSensor is None:
        partPlaced = Settings.PartSensor.CheckState().State.Value
    else:
        partPlaced = False

    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, "#Staging.RemovePart")
    PVA.Messaging.SetDialogIcon(dialogName, "UploadOutlineMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Blue")
    PVA.Messaging.SetDialogMessage(dialogName, "#Staging.OpenDoorRemovePartPrompt")
    PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#Process.AbortProcess", __cancelExecution__)
    PVA.Messaging.ShowDialogAsync(dialogName)

    isDoorOpen = not PVA.Safety.GetDoorClosed()
    while not isDoorOpen:
        isDoorOpen = not PVA.Safety.GetDoorClosed()
        if canceled:
            return
        while partPlaced == True and not Settings.PartSensor is None and not Inputs.BypassPartCheck.Value:
            if canceled:
                return
            partPlaced = Settings.PartSensor.CheckState().State.Value
            PVA.System.Wait(10)
        PVA.System.Wait(10)

    isDoorClosed = PVA.Safety.GetDoorClosed()
    if not Inputs.PlaceWhileRemoving.Value:
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.CloseDoorRemovePartPrompt")
    else:
        PVA.Messaging.SetDialogTitle(dialogName, "#Staging.ReplacePart")
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.CloseDoorReplacePartPrompt")
    while not isDoorClosed:
        if canceled:
            return
        isDoorClosed = PVA.Safety.GetDoorClosed()
        PVA.System.Wait(10)

    PVA.Safety.ResetDoorBypassOK()
    PVA.Safety.SetProcessDoorBlock(False)
    PVA.Safety.SetControlPowerOn()
    PVA.System.Wait(250)
    __servoMotors__()

    if not Inputs.PlaceWhileRemoving.Value:
        IsPartPlaced.Value = False

    PVA.Messaging.SetDialogButtonProperties(dialogName, 0, False, False, False, "#UI.Cancel", None)
    PVA.Messaging.CloseDialog(dialogName)

def __virtual__():
    pass

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

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Safety.SetProcessDoorBlock(False)
    PVA.Safety.ResetDoorBypassOK()
    IsPartPlaced.Value = False

def __exceptionrecovery__():
    pass

def __cancelExecution__():
    global canceled
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Safety.SetProcessDoorBlock(False)
    PVA.Safety.ResetDoorBypassOK()
    PVA.Safety.SetControlPowerOn()
    PVA.System.Wait(250)
    __servoMotors__()
    IsPartPlaced.Value = False
    PVA.Process.CancelExecution()
    canceled = True
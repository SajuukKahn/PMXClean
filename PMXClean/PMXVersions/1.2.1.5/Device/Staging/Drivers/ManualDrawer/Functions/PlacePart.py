#DisplayName = Place Part
#Description = Part handling routine that allows the use of the door bypass to manually load parts, and then awaits the cycle start input to continue execution flow
#Icon = DownloadOutlineMaterialIcon
#Flags = IsProcessStep, IsHidden

dialogName = "DrawerFunction"
canceled = False

def __inputs__():
    #Description = The robot to reserve when opening and closing the drawer
    Inputs.Robot = new.robot("Controller0", 0)

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
    partPlaced = False
    dialogOpen = False

    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitleWithParameters(dialogName, "#Staging.DrawerTitle", GetDisplayName())
    PVA.Messaging.SetDialogIcon(dialogName, "BlindsMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Blue")

    while not partPlaced:
        if not drawerExtended():
            if OpenDrawer(Inputs.Robot, new.bool(dialogOpen), new.bool(False)).Passed.Value == False:
                postCancelExecution(False)
                return

            dialogOpen = True;

        PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#Process.AbortProcess", __cancelExecution__)

        if not dialogOpen:
            PVA.Messaging.ShowDialogAsync(dialogName)
            dialogOpen = True

        if IsPartPlaced.Value:
            if Inputs.PlaceWhileRemoving.Value:
                PVA.Messaging.SetDialogMessage(dialogName, "#Staging.DrawerRemovePlacePart")
                IsPartPlaced.Value = True
            else:
                PVA.Messaging.SetDialogMessage(dialogName, "#Staging.DrawerRemovePart")
                IsPartPlaced.Value = False
        else:
            PVA.Messaging.SetDialogMessage(dialogName, "#Staging.DrawerPlacePart")
            IsPartPlaced.Value = True

        PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#UI.Continue", None)
        while not PVA.Messaging.CheckDialogInteraction(dialogName):
            PVA.System.Wait(25)

            if canceled:
                postCancelExecution(True)
                return

        PVA.System.Wait(100)
        if canceled:
            postCancelExecution(True)
            return

        PVA.Messaging.SetDialogButtonIsVisible(dialogName, 3, False)

        if CloseDrawer(Inputs.Robot, new.bool(True), new.bool(False)).Passed.Value == False:
            postCancelExecution(False)
            return

        PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#Process.AbortProcess", __cancelExecution__)

        pipsGood = True
        if Inputs.BypassPartCheck.Value == False:
            for pip in Settings.PartSensors:
                if hasattr(pip, "_PollState_"):
                    pipsGood = pipsGood and pip._PollState_.PolledState.Value

        partPlaced = pipsGood
        IsPartPlaced.Value = partPlaced

        if (not partPlaced):
            PVA.Messaging.SetDialogMessage(dialogName, "#Staging.PartNotFound")

            PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#UI.Continue", None)
            while not PVA.Messaging.CheckDialogInteraction(dialogName):
                PVA.System.Wait(25)
           
                if canceled:
                    postCancelExecution(True)
                    return
           
            PVA.System.Wait(100)
            if canceled:
                postCancelExecution(True)
                return
           
            PVA.Messaging.SetDialogButtonIsVisible(dialogName, 3, False)

    if Inputs.PlaceWhileRemoving.Value:
        if Settings.CycleStart is not None:
            PVA.Messaging.SetDialogMessage(dialogName, "#Staging.PressCycleStart")

            while Settings.CycleStart.Value != Settings.CycleStartOnState.Value:
                PVA.System.Wait(25)

                if canceled:
                    postCancelExecution(True)
                    return

            if canceled:
                postCancelExecution(True)
                return

        else:
            PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#Staging.CycleStart", None)
            PVA.Messaging.SetDialogMessage(dialogName, "#Staging.PressCycleStart")

            while not PVA.Messaging.CheckDialogInteraction(dialogName):
                PVA.System.Wait(25)

                if canceled:
                    postCancelExecution(True)
                    return

            if canceled:
                postCancelExecution(True)
                return

    PVA.Messaging.CloseDialog(dialogName)

def __virtual__():
    pass

def drawerExtended():
    return (Settings.FullyExtended._PollState_.PolledState.Value == True) and (Settings.FullyExtended._PollState_.IsSettled.Value == True)

def drawerRetracted():
    return (Settings.FullyRetracted._PollState_.PolledState.Value == True) and (Settings.FullyRetracted._PollState_.IsSettled.Value == True)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.NoInput = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    IsPartPlaced.Value = False

def __exceptionrecovery__():
    pass

def __cancelExecution__():
    global canceled
    canceled = True
    IsPartPlaced.Value = False

def postCancelExecution(openOrCloseDrawer):
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)

    if openOrCloseDrawer == True:
        OpenOrCloseDrawer(Inputs.Robot, new.bool(True))

    PVA.Process.CancelExecution()
#DisplayName = Open or Close Drawer
#Description = Unlocks the drawer to be fully opened or closed. Locks the drawer in when fully inserted or extended
#Icon = BlindsOpenMaterialIcon
#SubIcon = ArrowUpDownMaterialIcon
#Flags = IsTriggerStep
#ThreadSafe = True

def __inputs__():
    #Description = The robot to reserve axes 
    Inputs.Robot = new.robot("Controller0", 0)

def __run__():
    Outputs.Passed.Value = False

    processRunning = PVA.Process.IsProcessRunning()
    dialogName = GetReferenceName()

    if Inputs.Robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    if Settings.InteriorLock is None:
        __throwexception__(Exceptions.NoOutput, "Interior Lock")
        return

    if Settings.ExteriorLock is None:
        __throwexception__(Exceptions.NoOutput, "Exterior Lock")
        return

    if Settings.FullyRetracted is None:
        __throwexception__(Exceptions.NoInput, "Fully Retracted Input")
        return

    if Settings.FullyExtended is None:
        __throwexception__(Exceptions.NoInput, "Fully Extended Input")
        return

    if (Settings.FullyRetracted._PollState_.PolledState.Value == False) and (Settings.FullyExtended._PollState_.PolledState.Value == False):
        if Settings.GantryPower is not None:
            Inputs.Robot.WaitMotionComplete()
            Inputs.Robot.MotorOffAxes()

        Settings.InteriorLock.UnlockAndCheck(new.int(1000))
        Settings.ExteriorLock.UnlockAndCheck(new.int(1000))

        PVA.Messaging.CreateDialog(dialogName)
        PVA.Messaging.SetDialogTitleWithParameters(dialogName, "#Staging.DrawerTitle", GetDisplayName())
        PVA.Messaging.SetDialogIcon(dialogName, "BlindsOpenMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Blue")
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.OpenOrCloseDrawer")
        PVA.Messaging.SetDialogButtonIsVisible(dialogName, 0, False)
        PVA.Messaging.SetDialogButtonIsVisible(dialogName, 1, False)
        PVA.Messaging.SetDialogButtonIsVisible(dialogName, 2, False)
        PVA.Messaging.SetDialogButtonIsVisible(dialogName, 3, False)

        if processRunning:
            PVA.Messaging.SetProcessDialog(dialogName, PVA.Process.GetWorkflowIndex())
            PVA.Messaging.ShowProcessDialog(True, "Process")
        else:
            PVA.Messaging.ShowDialogAsync(dialogName)

        while (not drawerExtended() and not drawerRetracted()):
            PVA.System.Wait(50)

    if processRunning:
        PVA.Messaging.CloseProcessDialog(PVA.Process.GetWorkflowIndex())
    else:
        PVA.Messaging.CloseDialog(dialogName);

    if drawerExtended():
        if Settings.ExteriorLock.LockAndCheck(new.int(1000)).Passed.Value == True and Settings.GantryPower is not None:
            WaitForGantryPower(Inputs.Robot, new.double(3000))
    elif drawerRetracted():
        if Settings.InteriorLock.LockAndCheck(new.int(1000)).Passed.Value == True and Settings.GantryPower is not None:
            WaitForGantryPower(Inputs.Robot, new.double(3000))
    else:
        __throwexception__(Exceptions.OpenOrClosedFailed)
        return

    Outputs.Passed.Value = True

def __virtual__():
    pass

def drawerExtended():
    return (Settings.FullyExtended._PollState_.PolledState.Value == True) and (Settings.FullyExtended._PollState_.IsSettled.Value == True)

def drawerRetracted():
    return (Settings.FullyRetracted._PollState_.PolledState.Value == True) and (Settings.FullyRetracted._PollState_.IsSettled.Value == True)

def __outputs__():
    Outputs.Passed = new.bool(False, True)

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.NoInput = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.NoOutput = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OpenOrClosedFailed = new.exception("#Staging.Exceptions.DrawerExceptionTitle", "#Staging.Exceptions.OpenOrClosedFailed", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    dialogName = GetReferenceName()
    if PVA.Process.IsProcessRunning():
        PVA.Messaging.CloseProcessDialog(PVA.Process.GetWorkflowIndex())
    else:
        PVA.Messaging.CloseDialog(dialogName);
    Outputs.Passed.Value = False

def __exceptionrecovery__():
    pass

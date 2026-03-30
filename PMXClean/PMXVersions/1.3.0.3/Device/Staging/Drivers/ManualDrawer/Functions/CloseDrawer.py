#DisplayName = Close Drawer
#Description = Unlocks the drawer to be fully closed. Locks the drawer in when fully inserted
#Icon = BlindsOpenMaterialIcon
#SubIcon = ArrowUpThinMaterialIcon
#Flags = IsTriggerStep, IsProcessStep
#ThreadSafe = True

cancelled = False

def __inputs__():
    #Description = The robot to reserve axes 
    Inputs.Robot = new.robot("Controller0", 0)

    #Private = True
    #DisplayName = Kill Dialog
    #Description = A value indicating whether to kill the dialog at the end of this function
    Inputs.KillDialog = new.bool(True)

def __run__():
    global cancelled
    cancelled = False
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

    if Settings.FullyRetracted._PollState_.PolledState.Value == False:
        if Settings.GantryPower is not None:
            Inputs.Robot.WaitMotionComplete()
            Inputs.Robot.MotorOffAxes()

        Settings.InteriorLock.UnlockAndCheck(new.int(1000))
        Settings.ExteriorLock.UnlockAndCheck(new.int(1000))

        PVA.Messaging.CreateDialog(dialogName)

        if processRunning:
            PVA.Messaging.SetProcessDialog(dialogName, PVA.Process.GetWorkflowIndex())

        PVA.Messaging.SetDialogTitleWithParameters(dialogName, "#Staging.DrawerTitle", GetDisplayName())
        PVA.Messaging.SetDialogIcon(dialogName, "BlindsOpenMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Blue")
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.CloseDrawer")

        if processRunning:
            PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#Process.AbortProcess", __cancelExecution__)
            PVA.Messaging.ShowProcessDialog(True, "Process")
        else:
            PVA.Messaging.ShowDialogAsync(dialogName)

        while not drawerRetracted():
            PVA.System.Wait(50)

            if cancelled:
                onCancel()
                return

        if cancelled:
            onCancel()
            return

    if Inputs.KillDialog.Value:
        if processRunning:
            PVA.Messaging.CloseProcessDialog(PVA.Process.GetWorkflowIndex())
        else:
            PVA.Messaging.CloseDialog(dialogName)

    if Settings.InteriorLock.LockAndCheck(new.int(1000)).Passed.Value == True and Settings.GantryPower is not None:
        WaitForGantryPower(Inputs.Robot, new.double(3000))

    Outputs.Passed.Value = True

def __virtual__():
    pass

def drawerRetracted():
    return (Settings.FullyRetracted._PollState_.PolledState.Value == True) and (Settings.FullyRetracted._PollState_.IsSettled.Value == True)

def __outputs__():
    Outputs.Passed = new.bool(False, True)

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.NoInput = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.NoOutput = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global cancelled
    dialogName = GetReferenceName()
    if PVA.Process.IsProcessRunning():
        PVA.Messaging.CloseProcessDialog(PVA.Process.GetWorkflowIndex())
    else:
        PVA.Messaging.CloseDialog(dialogName)
    cancelled = True
    Outputs.Passed.Value = False

def __exceptionrecovery__():
    pass

def __cancelExecution__():
    global cancelled
    cancelled = True
    Outputs.Passed.Value = False

def onCancel():
    dialogName = GetReferenceName()
    PVA.Messaging.CloseProcessDialog(PVA.Process.GetWorkflowIndex())
    OpenOrCloseDrawer(Inputs.Robot, new.bool(False))
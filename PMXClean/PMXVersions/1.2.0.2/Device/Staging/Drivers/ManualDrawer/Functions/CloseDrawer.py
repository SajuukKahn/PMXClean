#DisplayName = Close Drawer
#Description = Unlocks the drawer to be fully closed. Locks the drawer in when fully inserted.
#Icon = BlindsOpenMaterialIcon
#SubIcon = ArrowUpThinMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

dialogName = "DrawerFunction"
canceled = False

def __inputs__():
    #Description = The robot to reserve axes 
    Inputs.Robot = new.robot("Controller0", 0)

    #Private = True
    #DisplayName = Dialog Already Open
    #Description = A value indicating whether the dialog is already open
    Inputs.DialogAlreadyOpen = new.bool(False)

    #Private = True
    #DisplayName = Kill Dialog
    #Description = A value indicating whether to kill the dialog at the end of this function
    Inputs.KillDialog = new.bool(True)

def __run__():
    global dialogName
    global canceled
    canceled = False
    Outputs.Passed.Value = False

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
        Inputs.Robot.MotorOffAxes()

        Settings.InteriorLock.UnlockAndCheck(new.int(1000))
        Settings.ExteriorLock.UnlockAndCheck(new.int(1000))

        if Inputs.DialogAlreadyOpen.Value == False:
            PVA.Messaging.CreateDialog(dialogName)

        PVA.Messaging.SetDialogTitleWithParameters(dialogName, "#Staging.DrawerTitle", GetDisplayName())
        PVA.Messaging.SetDialogIcon(dialogName, "BlindsOpenMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Blue")
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.CloseDrawer")

        if PVA.Process.IsProcessRunning():
            PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#Process.AbortProcess", __cancelExecution__)

        if Inputs.DialogAlreadyOpen.Value == False:
            PVA.Messaging.ShowDialogAsync(dialogName)

        while not drawerRetracted():
            PVA.System.Wait(50)

            if canceled:
                postCancelExecution()
                return

        if canceled:
            postCancelExecution()
            return

    if Inputs.KillDialog.Value:
        PVA.Messaging.CloseDialog(dialogName)

    if Settings.InteriorLock.LockAndCheck(new.int(1000)).Passed.Value == True:
        WaitForGantryPower(Inputs.Robot, new.double(3000))

    Outputs.Passed.Value = True

def __virtual__():
    pass

def drawerRetracted():
    return (Settings.FullyRetracted._PollState_.PolledState.Value == True) and (Settings.FullyRetracted._PollState_.IsSettled.Value == True)

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
    Outputs.Passed = new.bool(False)

def __lockresources__():
    if Inputs.Robot is not None:
        Inputs.Robot.RequestMove()
        Inputs.Robot.Reserve()

def __releaseresources__():
    if Inputs.Robot is not None:
        Inputs.Robot.Release()
        Inputs.Robot.MoveComplete()

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.NoInput = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.NoOutput = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global canceled
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Process.CancelExecution()
    canceled = True
    Outputs.Passed.Value = False
    __releaseresources__()

def __exceptionrecovery__():
    pass

def __cancelExecution__():
    global canceled
    canceled = True
    Outputs.Passed.Value = False

def postCancelExecution():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    OpenOrCloseDrawer(Inputs.Robot, new.bool(False))
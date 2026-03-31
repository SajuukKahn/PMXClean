#DisplayName = Park In Solvent
#Description = Park the Robot in a designated location
#Icon = CupWaterMaterialIcon
#SubIcon = CursorMoveMaterialIcon
#Groups = Motion
#Flags = IsHidden

dialogName = "parkInSolvent"

def __inputs__():
    #DisplayName = Solvent Location
    #Description = The location that is configured for parking in solvent
    Inputs.SolventLocation = new.robotlocation("Controller0", 0)
    
    #DisplayName = Show Status Message
    #Description = A value indicating whether the function should show a message to the user while moving
    Inputs.ShowStatusMessage = new.bool(False)

def __run__():
    global dialogName

    robot = new.robot(Inputs.SolventLocation.DeviceName, Inputs.SolventLocation.RobotIndex)

    if Inputs.SolventLocation is None:
        __throwexception__(Exceptions.LocationNotFound, "#Controller.Solvent")
        return

    if not Inputs.SolventLocation.LocationHasBeenTaught:
        __throwexception__(Exceptions.LocationNotTaught, "#Controller.Solvent")
        return

    if "CheckTimerAndCancel" in globals():
        if not CheckTimerAndCancel():
            if robot is not None:
                robot.ReleaseExtendedLock()
            return

    robot.IsParked.Value = True

    PVA.Tools.AllUp()
    robot.IsPostParkComplete.Value = False

    if (Inputs.ShowStatusMessage.Value):
        PVA.Messaging.CreateDialog(dialogName)
        PVA.Messaging.SetDialogIcon(dialogName, "CursorMoveMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
        PVA.Messaging.SetDialogTitle(dialogName, "#Controller.MoveToSolvent")
        PVA.Messaging.SetDialogMessage(dialogName, robot.GetDisplayName() + " #Controller.MovingTo " + Inputs.SolventLocation.DisplayName + ". #UI.PleaseWait")
        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
        PVA.Messaging.ShowDialogAsync(dialogName)

    SetLocationSpeeds(robot, Inputs.SolventLocation)
    InternalSafeMoveRobotToPosition(robot, Inputs.SolventLocation.Coordinate)

    PVA.Messaging.CloseDialog(dialogName)

    PVA.Tools.AllDown()
    PVA.Pendants.Lock()

    while not robot.IsMoveRequested.Value:
        PVA.System.Wait(10)

    robot.IsPostParkComplete.Value = True

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.LocationNotFound = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotFound", new.enum("Severity", "Error").Value, None)
    Exceptions.LocationNotTaught = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotTaught", new.enum("Severity", "Error").Value, None)

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.SolventLocation is not None:
        robot = new.robot(Inputs.SolventLocation.DeviceName, Inputs.SolventLocation.RobotIndex)
        if robot is not None:
            robot.PriorityReserve()
            robot.ReserveExtendedLock()

def __releaseresources__():
    if Inputs.SolventLocation is not None:
        robot = new.robot(Inputs.SolventLocation.DeviceName, Inputs.SolventLocation.RobotIndex)
        if robot is not None:
            robot.Release()
    PVA.Safety.ResetDoorBypassOK()

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    if Inputs.SolventLocation is not None:
        robot = new.robot(Inputs.SolventLocation.DeviceName, Inputs.SolventLocation.RobotIndex)
        if robot is not None:
            InternalStopRobot(robot)
            robot.Release()
            robot.ReleaseExtendedLock()
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Pendants.Unlock()

def __exceptionrecovery__():
    if Inputs.SolventLocation is not None:
        robot = new.robot(Inputs.SolventLocation.DeviceName, Inputs.SolventLocation.RobotIndex)
        if robot is not None:
            robot.IsParked.Value = False
            robot.IsPostParkComplete.Value = True
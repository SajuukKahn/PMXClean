#DisplayName = Move To Location
#Description = Move the robot to a taught location
#Icon = CursorMoveMaterialIcon
#Groups = Motion
#Flags = IsTriggerStep, IsProcessStep, IsHidden

dialogName = None

def __inputs__():
    #Description = The location to move to
    Inputs.Location = new.robotlocation("Controller0", 0, 0)
    
    #DisplayName = Show Status Message
    #Description = A value indicating whether the function should show a message to the user while moving
    Inputs.ShowStatusMessage = new.bool(False)

    #Private = True
    #DisplayName = Settle Counts
    #Description = The amount of counts to settle to
    Inputs.SettleCounts = new.double(5, 0, 50, 1, 1, "counts")

    #Private = True
    #DisplayName = Settle Time
    #Description = The minimum time to be at the given settle counts before resuming
    Inputs.SettleTime = new.double(50, 0, 5000, 1, 10, "ms")


def __run__():
    global dialogName
    dialogName = None
    if Inputs.Location is None:
        PVA.Exceptions.ThrowException(Exceptions.LocationNotFound)
        return

    if not Inputs.Location.LocationHasBeenTaught:
        PVA.Exceptions.ThrowException(Exceptions.LocationNotTaught, Inputs.Location.DisplayName)
        return

    robot = new.robot(Inputs.Location.DeviceName, Inputs.Location.RobotIndex)

    if (Inputs.ShowStatusMessage.Value):
        dialogName = PVA.Messaging.CreateUniqueDialog()
        PVA.Messaging.SetDialogIcon(dialogName, "CursorMoveMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
        PVA.Messaging.SetDialogTitle(dialogName, "#Controller.MoveToLocation")
        PVA.Messaging.SetDialogMessage(dialogName, robot.GetDisplayName() + " #Controller.MovingTo " + Inputs.Location.DisplayName + ". #UI.PleaseWait")
        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
        PVA.Messaging.ShowDialogAsync(dialogName)

    SetLocationSpeeds(robot, Inputs.Location)
    SafeMoveRobotToPosition(robot, Inputs.Location.Coordinate, Inputs.SettleCounts, Inputs.SettleTime)

    if dialogName is not None:
        PVA.Messaging.CloseDialog(dialogName)
        dialogName = None

def __virtual__():
    pass

def __outputs__():
    pass

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.Location is not None:
        robot = new.robot(Inputs.Location.DeviceName, Inputs.Location.RobotIndex)
        if robot is not None:
            robot.RequestMove()
            robot.Reserve()

def __releaseresources__():
    if Inputs.Location is not None:
        robot = new.robot(Inputs.Location.DeviceName, Inputs.Location.RobotIndex)
        if robot is not None:
            robot.Release()
            robot.MoveComplete()
    PVA.Safety.ResetDoorBypassOK()

def __exceptions__():
    Exceptions.LocationNotFound = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotFound", new.enum("Severity", "Error").Value, None)
    Exceptions.LocationNotTaught = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotTaught", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    if (dialogName is not None):
        PVA.Messaging.CloseDialog(dialogName)
        dialogName = None

def __exceptionrecovery__():
    pass
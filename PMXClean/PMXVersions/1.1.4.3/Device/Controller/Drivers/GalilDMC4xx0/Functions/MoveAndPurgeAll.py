# DisplayName = Move and Purge All
# Description = Move the Robot to the designated purge location and execute AllDown and AllOn
# Icon = SprinklerFireMaterialIcon
# SubIcon = CursorMoveMaterialIcon
# Groups = Motion
# Flags = IsHidden

dialogName = "moveAndPurgeAll"

def __inputs__():
    #DisplayName = Purge Location
    #Description = The location that is configured for purging
    Inputs.PurgeLocation = new.robotlocation("Controller0", 0)
    
    #DisplayName = Purge Time
    #Description = The amount of time to purge for
    Inputs.PurgeTime = new.int(1000, 0, 1000000, 10, 100, "ms")
    
    #DisplayName = Show Status Message
    #Description = A value indicating whether the function should show a message to the user while moving
    Inputs.ShowStatusMessage = new.bool(False)

def __run__():
    global dialogName

    robot = new.robot(Inputs.PurgeLocation.DeviceName, Inputs.PurgeLocation.RobotIndex)

    if Inputs.PurgeLocation is None:
        __throwexception__(Exceptions.LocationNotFound, "#Controller.Purge")
        return

    if not Inputs.PurgeLocation.LocationHasBeenTaught:
        __throwexception__(Exceptions.LocationNotTaught, "#Controller.Purge")
        return

    robot.IsParked.Value = False
    PVA.Tools.AllUp()

    if (Inputs.ShowStatusMessage.Value):
        PVA.Messaging.CreateDialog(dialogName)
        PVA.Messaging.SetDialogIcon(dialogName, "CursorMoveMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
        PVA.Messaging.SetDialogTitle(dialogName, "#Controller.MoveToPurge")
        PVA.Messaging.SetDialogMessage(dialogName, robot.GetDisplayName() + " #Controller.MovingTo " + Inputs.PurgeLocation.DisplayName + ". #UI.PleaseWait")
        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
        PVA.Messaging.ShowDialogAsync(dialogName)

    SetLocationSpeeds(robot, Inputs.PurgeLocation)
    InternalSafeMoveRobotToPosition(robot, Inputs.PurgeLocation.Coordinate)
    
    if (Inputs.ShowStatusMessage.Value):
        PVA.Messaging.SetDialogMessage(dialogName, "#Controller.Purging, #UI.PleaseWait")

    PVA.Tools.AllDown()
    PVA.Tools.AllOn()
    PVA.System.Wait(Inputs.PurgeTime.Value)
    PVA.Tools.AllOff()
    PVA.Tools.AllUp()

    PVA.Messaging.CloseDialog(dialogName)

    InternalSafeMoveRobotToPosition(robot, new.coordinate(None, None, robot.SafeZ, None))
    PVA.Pendants.Unlock()

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.LocationNotFound = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotFound", new.enum("Severity", "Error").Value, None)
    Exceptions.LocationNotTaught = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotTaught", new.enum("Severity", "Error").Value, None)

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.PurgeLocation is not None:
        robot = new.robot(Inputs.PurgeLocation.DeviceName, Inputs.PurgeLocation.RobotIndex)
        if robot is not None:
            robot.RequestMove()
            robot.PriorityReserve()

def __releaseresources__():
    if Inputs.PurgeLocation is not None:
        robot = new.robot(Inputs.PurgeLocation.DeviceName, Inputs.PurgeLocation.RobotIndex)
        if robot is not None:
            robot.Release()
            robot.ReleaseExtendedLock()
            robot.MoveComplete()
    PVA.Safety.ResetDoorBypassOK()

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    if Inputs.PurgeLocation is not None:
        robot = new.robot(Inputs.PurgeLocation.DeviceName, Inputs.PurgeLocation.RobotIndex)
        if robot is not None:
            InternalStopRobot(robot)
            robot.Release()
            robot.ReleaseExtendedLock()
    PVA.Tools.AllOff()
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Pendants.Unlock()

def __exceptionrecovery__():
    if Inputs.PurgeLocation is not None:
        robot = new.robot(Inputs.PurgeLocation.DeviceName, Inputs.PurgeLocation.RobotIndex)
        if robot is not None:
            robot.IsParked.Value = False
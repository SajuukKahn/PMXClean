# DisplayName = Clean Tools
# Description = Optionally park the Robot in a designated location, then optionally move the Robot to the designated purge location and execute AllDown and AllOn
# Icon = SprinklerFireMaterialIcon
# SubIcon = CupWaterMaterialIcon
# Groups = Motion
# Flags = IsTriggerStep, IsHidden

dialogName = "cleanTools"

def __inputs__():
    #Optional = True
    #DisplayName = Solvent Location
    #Description = The location that is configured for parking in solvent
    Inputs.SolventLocation = new.robotlocation("Controller0", 0, 2)
    Inputs.SolventLocation.IsEnabled = False

    #Optional = True
    #DisplayName = Purge Location
    #Description = The location that is configured for purging
    Inputs.PurgeLocation = new.robotlocation("Controller0", 0, 1)

    #DisplayName = Purge Time
    #Description = The amount of time to purge for
    Inputs.PurgeTime = new.int(1000, 0, 1000000, 10, 100, "ms")

    #DisplayName = Show Status Message
    #Description = A value indicating whether the function should show a message to the user while moving
    Inputs.ShowStatusMessage = new.bool(False)

def __run__():
    global dialogName

    solventLocation = Inputs.SolventLocation
    purgeLocation = Inputs.PurgeLocation

    if solventLocation is None and purgeLocation is None:
        __throwexception__(Exceptions.LocationRequired)
        return
        
    if solventLocation is not None and not solventLocation.LocationHasBeenTaught:
        __throwexception__(Exceptions.LocationNotTaught, "#Controller.Solvent")
        return
        
    if purgeLocation is not None and not purgeLocation.LocationHasBeenTaught:
        __throwexception__(Exceptions.LocationNotTaught, "#Controller.Purge")
        return

    if solventLocation is not None:
        robot = new.robot(solventLocation.DeviceName, solventLocation.RobotIndex)
        if "CheckTimerAndCancel" in globals():
            if not CheckTimerAndCancel():
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

        SetLocationSpeeds(robot, solventLocation)
        InternalSafeMoveRobotToPosition(robot, solventLocation.Coordinate)

        PVA.Messaging.CloseDialog(dialogName)

        PVA.Tools.AllDown()

        while not robot.IsMoveRequested.Value:
            PVA.System.Wait(10)

        if purgeLocation is None:
            robot.IsParked.Value = False
            PVA.Tools.AllUp()
            robot.IsPostParkComplete.Value = True

    if purgeLocation is not None:
        robot = new.robot(purgeLocation.DeviceName, purgeLocation.RobotIndex)
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

        SetLocationSpeeds(robot, purgeLocation)
        InternalSafeMoveRobotToPosition(robot, purgeLocation.Coordinate)
        
        if (Inputs.ShowStatusMessage.Value):
            PVA.Messaging.SetDialogMessage(dialogName, "#Controller.Purging, #UI.PleaseWait")

        PVA.Tools.AllDown()
        PVA.Tools.AllOn()
        PVA.System.Wait(Inputs.PurgeTime.Value)
        PVA.Tools.AllOff()
        PVA.Tools.AllUp()

        PVA.Messaging.CloseDialog(dialogName)
        robot.IsPostParkComplete.Value = True

        InternalSafeMoveRobotToPosition(robot, new.coordinate(None, None, robot.SafeZ, None))


def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.LocationRequired = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.OneLocationRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.LocationNotTaught = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotTaught", new.enum("Severity", "Error").Value, None)

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    PVA.Pendants.Lock()
    location = Inputs.SolventLocation or Inputs.PurgeLocation
    if (location is not None):
        robot = new.robot(location.DeviceName, location.RobotIndex)
        if robot is not None:
            robot.Reserve()

def __releaseresources__():
    PVA.Safety.ResetDoorBypassOK()
    PVA.Pendants.Unlock()
    location = Inputs.SolventLocation or Inputs.PurgeLocation
    if (location is not None):
        robot = new.robot(location.DeviceName, location.RobotIndex)
        if robot is not None:
            robot.Release()

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    location = Inputs.SolventLocation or Inputs.PurgeLocation
    if (location is not None):
        robot = new.robot(location.DeviceName, location.RobotIndex)
        if robot is not None:
            robot.Release()
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Pendants.Unlock()

def __exceptionrecovery__():
    location = Inputs.SolventLocation or Inputs.PurgeLocation
    if (location is not None):
        robot = new.robot(location.DeviceName, location.RobotIndex)
        if robot is not None:
            robot.IsParked.Value = False
            robot.IsPostParkComplete.Value = True
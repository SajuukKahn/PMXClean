#DisplayName = Move and Vacuum Purge
#Description = Move the Tool to the designated vacuum purge location, then purge the tool while suction is on
#Icon = SprinklerFireMaterialIcon
#SubIcon = CursorMoveMaterialIcon
#Flags = IsHidden, IsTriggerStep

dialogName = "VacuumPurge"

def __inputs__():
    #Description = The tool to purge.
    Inputs.Tool = new.tool(0)

    #Description = The vacuum purge location to move the tool to.
    Inputs.Location = new.toollocation("Controller0", 0, -1)

    #DisplayName = Purge Time
    #Description = The amount of time to purge for
    Inputs.PurgeTime = new.int(1000, 0, 1000000, 10, 100, "ms")
    
    #DisplayName = Show Status Message
    #Description = A value indicating whether the function should show a message to the user while moving
    Inputs.ShowStatusMessage = new.bool(True)

    #DisplayName = Wait for Vacuum Pressure
    #Description = A value indicating whether to wait for the vacuum analog input to reach 1.5x it's starting value, and error if that value hasn't been reached in the timeout.
    Inputs.WaitForVacuumPressure = new.bool(True)

    #DisplayName = Vacuum Pressure Timeout
    #Description = The timeout used when waiting for vacuum pressure to reach 1.5x it's original value.
    Inputs.VacuumPressureTimeout = new.int(4000, 0, 1000000, 10, 100, "ms")

def __run__():
    global dialogName

    settleCounts = new.double(5, 0, 50, 1, 1, "counts")
    settleTime = new.double(50, 0, 5000, 1, 10, "ms")

    robot = new.robot(Inputs.Location.DeviceName, Inputs.Location.RobotIndex)
    controller = robot.GetController()

    if controller is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    if Inputs.Tool is None:
        __throwexception__(Exceptions.ToolRequired)
        return

    if not Inputs.Tool.IsOnZAxis() or not Inputs.Tool.IsOffsetTaught():
        __throwexception__(Exceptions.ToolCannotBeCalibrated)
        return

    if Settings.VacuumOutput is None:
        __throwexception__(Exceptions.VacuumOutputMissing)
        return

    if Settings.AnalogInput is None:
        __throwexception__(Exceptions.AnalogInputMissing)
        return

    if Inputs.Location is None:
        __throwexception__(Exceptions.LocationNotFound, "#Cleaning.VacuumPurge")
        return

    if not Inputs.Location.LocationHasBeenTaught:
        __throwexception__(Exceptions.LocationNotTaught, "#Cleaning.VacuumPurge")
        return

    controller.MoveToSafeZ(robot)
    PVA.Tools.AllUp()

    if (Inputs.ShowStatusMessage.Value):
        PVA.Messaging.CreateDialog(dialogName)
        PVA.Messaging.SetDialogIcon(dialogName, "CursorMoveMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
        PVA.Messaging.SetDialogTitle(dialogName, "#Cleaning.MoveToVacuumPurge")
        PVA.Messaging.SetDialogMessage(dialogName, robot.GetDisplayName() + " #Controller.MovingTo " + Inputs.Location.DisplayName + ". #UI.PleaseWait")
        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
        PVA.Messaging.ShowDialogAsync(dialogName)

    controller.SetLocationSpeeds(robot, Inputs.Location)
    controller.SafeMoveRobotToPosition(robot, new.coordinate(None, None, None, 0), settleCounts, settleTime)

    location = Inputs.Location.Coordinate + Inputs.Tool.GetOffset(0)
    controller.MoveRobotToPosition(robot, new.coordinate(location.X.Value, location.Y.Value, None, None), settleCounts, settleTime)
    controller.MoveRobotToPosition(robot, new.coordinate(None, None, location.Z.Value, None), settleCounts, settleTime)

    if (Inputs.ShowStatusMessage.Value):
        PVA.Messaging.SetDialogMessage(dialogName, "#Controller.Purging, #UI.PleaseWait")

    On()
    Inputs.Tool.TryExecuteFunction("Down")

    if Inputs.WaitForVacuumPressure.Value:
        startingVoltage = Settings.AnalogInput.Value
        timeout = PVA.System.GetCurrentTime().Value + Inputs.VacuumPressureTimeout.Value

        while (Settings.AnalogInput.Value < (startingVoltage * 1.5)) and (PVA.System.GetCurrentTime().Value < timeout):
            PVA.System.Wait(50)

        if Settings.AnalogInput.Value < (startingVoltage * 1.5):
            __throwexception__(Exceptions.VacuumPressureTimeoutException)
            
    Inputs.Tool.TryExecuteFunction("On")
    PVA.System.Wait(Inputs.PurgeTime.Value)
    Inputs.Tool.TryExecuteFunction("Off")
    Off()
    Inputs.Tool.TryExecuteFunction("Up")

    PVA.Messaging.CloseDialog(dialogName)

    controller.MoveToSafeZ(robot)
    PVA.Pendants.Unlock()

def __virtual__():
    PVA.System.Wait(Inputs.PurgeTime.Value)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.ToolRequired = new.exception("#Tool.Exceptions.NoToolTitle", "#Tool.Exceptions.NoTool", new.enum("Severity", "Error").Value, None)
    Exceptions.ToolCannotBeCalibrated = new.exception("#Tool.Exceptions.CannotBeCalibratedTitle", "#Tool.Exceptions.CannotBeCalibrated", new.enum("Severity", "Error").Value, None)
    Exceptions.VacuumOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.AnalogInputMissing = new.exception("#IO.Exceptions.AnalogInputMissingTitle", "#IO.Exceptions.AnalogInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.LocationNotFound = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotFound", new.enum("Severity", "Error").Value, None)
    Exceptions.LocationNotTaught = new.exception("#Controller.Exceptions.LocationErrorTitle", "#Controller.Exceptions.LocationNotTaught", new.enum("Severity", "Error").Value, None)
    Exceptions.VacuumPressureTimeoutException = new.exception("#Cleaning.Exceptions.VacuumPurgeTitle", "#Cleaning.Exceptions.VacuumPressureTimeoutException", new.enum("Severity", "Error").Value, None)

def __lockresources__():
    PVA.Safety.SetDoorBypassOK(False)
    if Inputs.Tool.GetRobot() is not None:
        Inputs.Tool.GetRobot().Reserve()

def __releaseresources__():
    if Inputs.Tool.GetRobot() is not None:
        Inputs.Tool.GetRobot().Release()

def __throwexception__(exception, name = ""):
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    if Inputs.Tool.GetRobot() is not None:
        Inputs.Tool.GetRobot().Release()

def __exceptionrecovery__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
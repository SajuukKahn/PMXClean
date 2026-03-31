#DisplayName = Wait for Gantry Power
#Description = Waits for gantry power to be on and then releases the robot
#Icon = DownloadOutlineMaterialIcon
#Flags = IsHidden

dialogName = "DrawerFunction"

def __inputs__():
    #Description = The robot to reserve axes 
    Inputs.Robot = new.robot("Controller0", 0)

    #Description = The maximum amount of time to wait for the door to reach the desired state
    Inputs.Timeout = new.int(3000, 0, 1000000, 10, 100, "ms")

def __run__():
    if Inputs.Robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
    while (Settings.GantryPower.Value != Settings.GantryPowerOnState.Value) and (PVA.System.GetCurrentTime().Value < timeout):
        PVA.System.Wait(50)

    if Settings.GantryPower.Value != Settings.GantryPowerOnState.Value:
        __throwexception__(Exceptions.FailedToGetGantryPower)
        return

    Inputs.Robot.ServoAxes()

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.FailedToGetGantryPower = new.exception("#Staging.Exceptions.DrawerExceptionTitle", "#Staging.Exceptions.FailedToGetGantryPower", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)

def __exceptionrecovery__():
    pass
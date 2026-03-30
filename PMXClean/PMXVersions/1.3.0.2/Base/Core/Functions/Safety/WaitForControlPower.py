#DisplayName = Wait for Control Power
#Description = Waits for control power to be on
#Icon = DownloadOutlineMaterialIcon
#Flags = IsHidden

def __inputs__():
    #Description = The maximum amount of time to wait for control power to reach the desired state
    Inputs.Timeout = new.int(3000, 0, 1000000, 10, 100, "ms")

def __run__():

    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
    while (not GetControlPowerOn()) and (PVA.System.GetCurrentTime().Value < timeout):
        PVA.System.Wait(50)

    Outputs.Passed.Value = GetControlPowerOn()

def __virtual__():
    pass

def __outputs__():
    Outputs.Passed = new.bool(False, True)

def __exceptions__():
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
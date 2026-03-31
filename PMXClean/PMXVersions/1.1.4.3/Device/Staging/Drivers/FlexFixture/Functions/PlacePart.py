# DisplayName = Place Part
# Description = Part handling routine that allows the use of the door bypass to manually load parts, and then awaits the cycle start input to continue execution flow
# Icon = DownloadOutlineMaterialIcon
# Flags = IsProcessStep

dialogName = "PlacePart"
canceled = False

def __inputs__():
    #Optional = True
    #Enabled = False
    #DisplayName = Part Sensor
    #Description = The optional sensor that must be on for the code execution to continue
    Inputs.PartSensor = new.device("PIP", 0)
    
    #DisplayName = Bypass Part Check
    #Description = A value indicating whether to skip checking for part presence
    Inputs.BypassPartCheck = new.bool(True)
    
    #DisplayName = Cycle Start
    #Description = The cycle start input that must be in the defined On State to continue code execution
    Inputs.CycleStart = new.input()
    
    #DisplayName = Cycle Start On State
    #Description = A value indicating the required input state of the Cycle Start input in order to be considered On
    Inputs.CycleStartOnState = new.bool(False, True)

def __run__():
    global dialogName
    global canceled
    canceled = False
    if Inputs.CycleStart is None:
        __throwexception__(Exceptions.NoInput, "Cycle Start Input")

    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, "#Staging.PlacePart")
    PVA.Messaging.SetDialogIcon(dialogName, "DownloadOutlineMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Blue")
    PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#Process.AbortProcess", __cancelExecution__)
    PVA.Messaging.ShowDialogAsync(dialogName)

    partPlaced = IsPartPlaced.Value
    if not partPlaced:
        stopMotors()
        PVA.System.Wait(250)
        PVA.Safety.SetControlPowerOff()
        PVA.Safety.SetProcessDoorBlock(True)
        PVA.Safety.SetDoorBypassOK(True)
        if not Inputs.PartSensor is None:
            partPlaced = Inputs.PartSensor.CheckState().State.Value
        else:
            partPlaced = False

        isDoorOpen = not PVA.Safety.GetDoorClosed()
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.OpenDoorPlacePartPrompt")
        while not isDoorOpen:
            isDoorOpen = not PVA.Safety.GetDoorClosed()
            if canceled:
                return
            while partPlaced == False and not Inputs.PartSensor is None and not Inputs.BypassPartCheck.Value:
                if canceled:
                    return
                partPlaced = Inputs.PartSensor.CheckState().State.Value
                PVA.System.Wait(10)
            PVA.System.Wait(10)

        isDoorClosed = PVA.Safety.GetDoorClosed()
        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.CloseDoorPlacePartPrompt")
        while not isDoorClosed:
            if canceled:
                return
            isDoorClosed = PVA.Safety.GetDoorClosed()
            PVA.System.Wait(10)

        PVA.Safety.ResetDoorBypassOK()
        PVA.Safety.SetProcessDoorBlock(False)
        PVA.Safety.SetControlPowerOn()
        PVA.System.Wait(250)
        __servoMotors__()

        IsPartPlaced.Value = True

    startPressed = Inputs.CycleStart.Value == Inputs.CycleStartOnState.Value
    PVA.Messaging.SetDialogMessage(dialogName, "#Staging.CycleStart")
    while not startPressed:
        if canceled:
            return
        startPressed = Inputs.CycleStart.Value == Inputs.CycleStartOnState.Value
        PVA.System.Wait(10)
    
    PVA.Messaging.SetDialogButtonProperties(dialogName, 0, False, False, False, "#UI.Cancel", None)
    PVA.Messaging.CloseDialog(dialogName)

def __virtual__():
    pass

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
    pass

def __exceptions__():
    Exceptions.NoInput = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Safety.SetProcessDoorBlock(False)
    PVA.Safety.ResetDoorBypassOK()
    IsPartPlaced.Value = False

def __exceptionrecovery__():
    pass

def __cancelExecution__():
    global canceled
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Safety.SetProcessDoorBlock(False)
    PVA.Safety.ResetDoorBypassOK()
    PVA.Safety.SetControlPowerOn()
    PVA.System.Wait(250)
    __servoMotors__()
    IsPartPlaced.Value = False
    PVA.Process.CancelExecution()
    canceled = True
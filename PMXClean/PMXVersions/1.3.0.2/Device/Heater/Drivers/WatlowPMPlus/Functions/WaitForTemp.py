#DisplayName = Wait For Temperature
#Description = Waits for the heater to reach the set point
#Icon = FireMaterialIcon
#SubIcon = TimerOutlineMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

dialogName = ""
canceled = False

def __inputs__():
    #DisplayName = Desired Temperature
    #Description = The temperature to wait for the heater to heat up to
    #CanReference = True
    Inputs.DesiredTemperature = new.double(0, 0, 70, 0.1, 1, "[Unit]", __source__)

def __run__():
    global dialogName
    global canceled
    canceled = False

    Outputs.AtTemp.Value = False
    currentTemp = ConvertUnits(GetTemperature().Temperature.Value)
    desiredTemp = ConvertUnits(Inputs.DesiredTemperature.Value)
    
    if currentTemp is not None:
        if currentTemp < desiredTemp:
            dialogName = PVA.Messaging.CreateUniqueDialog(dialogName)
            PVA.Messaging.SetDialogTitle(dialogName, "#Heater.WaitForTempTitle")
            PVA.Messaging.SetDialogIcon(dialogName, "ThermometerMaterialIcon")
            updateDialog(currentTemp, desiredTemp)
            PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
            PVA.Messaging.SetDialogProgressBarTime(dialogName, 0)
            PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#UI.Cancel", __cancelExecution__)
            PVA.Messaging.ShowDialogAsync(dialogName)

            while currentTemp < desiredTemp:
                currentTemp = ConvertUnits(GetTemperature().Temperature.Value)

                PVA.System.Wait(100)
                updateDialog(currentTemp, desiredTemp)
                if canceled:
                    return

            PVA.Messaging.CloseDialog(dialogName)

        Outputs.AtTemp.Value = True
        
def __virtual__():
    pass

def updateDialog(currentTemp, desiredTemp):
    global dialogName
    units = GetTemperatureUnits()
    PVA.Messaging.SetDialogMessageWithParameters(dialogName, "#Heater.WaitForTemp", GetDisplayName(), '{:.2f}'.format(desiredTemp) + units, '{:.2f}'.format(currentTemp) + units)

def __outputs__():
    #DisplayName = At Desired Temperature
    #Description = A value indicating whether this heater device has reached the desired temperature
    Outputs.AtTemp = new.bool(False, True)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

def __cancelExecution__():
    global canceled
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    PVA.Process.CancelExecution()
    canceled = True
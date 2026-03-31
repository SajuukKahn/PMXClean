#DisplayName = Update Desired Temperature and Deviation
#Description = Update the desired temperature and deviation allowed for a specific application
#Icon = UpdateMaterialIcon
#Flags = IsProcessStep, IsProgramStep, IsHidden

def __inputs__():
    #DisplayName = Desired Temperature
    #Description = The desired temperature that must be maintained
    Inputs.DesiredTemperature = new.double(0, 0, 70, 0.1, 1, "[Unit]", __source__)

    #Description = The temperature deviation that will be allowed
    Inputs.Deviation = new.double(0, 0, 100, 0.1, 1, "%")

def __run__():
    deviceParameter = GetDeviceParameter()
    newTemp = float('nan')
    if Inputs.DesiredTemperature is not None:
        newTemp = Inputs.DesiredTemperature.Value
    deviation = float('nan')
    if Inputs.Deviation is not None:
        deviation = Inputs.Deviation.Value
    PVA.Heaters.UpdateTemperatureMonitorSettings(deviceParameter, newTemp, deviation, None)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
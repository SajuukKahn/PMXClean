# DisplayName = Update Pressure Min/Max Settings
# Description = Update the minimum and maximum pressure range allowed for a specific application
# Icon = UpdateMaterialIcon
# Flags = IsProcessStep, IsProgramStep, IsHidden

def __inputs__():
    #Optional = True
    #Description = The minimum pressure that must be maintained
    Inputs.Low = new.double(0, -32748, 32747, 0.1, 1, "[Unit]", __source__)

    #Optional = True
    #Description = The maximum pressure that cannot be exceeded
    Inputs.High = new.double(0, -32748, 32747, 0.1, 1, "[Unit]", __source__)

def __run__():
    deviceParameter = GetDeviceParameter()
    newLow = float('nan')
    if Inputs.Low is not None:
        newLow = Inputs.Low.Value
    newHigh = float('nan')
    if Inputs.High is not None:
        newHigh = Inputs.High.Value
    PVA.Sensors.UpdateAnalogSensorSettings(deviceParameter, newLow, newHigh, None)

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
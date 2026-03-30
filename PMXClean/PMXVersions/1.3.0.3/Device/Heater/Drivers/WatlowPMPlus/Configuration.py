def __settings__():
    #DisplayName = Temperature Low Limit
    #Private = True
    Settings.LowLimit = new.double(0, 0, 500, 0.1, 1, "[Unit]", __source__)
    Settings.LowLimit.DisableUnitProviderMinMax = True

    #DisplayName = Temperature High Limit
    #Private = True
    Settings.HighLimit = new.double(100, 0, 500, 0.1, 1, "[Unit]", __source__)
    Settings.HighLimit.DisableUnitProviderMinMax = True

    #DisplayName = Critical Over Temperature
    #Private = True
    Settings.CriticalOverTemp = new.double(200, 0, 500, 0.1, 1, "[Unit]", __source__)
    Settings.CriticalOverTemp.DisableUnitProviderMinMax = True

    #Optional = True
    #DisplayName = Heater On
    Settings.HeaterOnOutput = new.output()

    #Optional = True
    #DisplayName = Over Temperature
    Settings.OverTempInput = new.input()

    #DisplayName = Over Temperature State
    Settings.OverTempState = new.bool(False)

def onconnect():
    # Check device for hardware failure
    if (AnalogInputError()):
        raise

    # Set Word Order to Low High
    SendPacket(BuildModbusPacket(16, 2488, 1331))

    # Set Communication Display Units to Celsius
    SendPacket(BuildModbusPacket(16, 2490, 15))

    UpdateSetPoint(GetSetPoint().SetPoint.Value)

    Off()

def ondisconnect():
    Off()
    TemperatureMonitoring()

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
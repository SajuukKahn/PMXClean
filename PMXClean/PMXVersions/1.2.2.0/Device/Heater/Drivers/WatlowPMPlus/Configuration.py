def __settings__():
    Settings.Address = new.int(1, 0, 256, 1, 10)

    #DisplayName = Temperature Low Limit
    Settings.LowLimit = new.double(0, 0, 300, 0.1, 1, "[Unit]", __source__)

    #DisplayName = Temperature High Limit
    Settings.HighLimit = new.double(70, 0, 300, 0.1, 1, "[Unit]", __source__)

    #DisplayName = Critical Over Temperature
    Settings.CriticalOverTemp = new.double(300, 0, 300, 0.1, 1, "[Unit]", __source__)

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
    SendPacket(BuildModbusPacket(Settings.Address.Value, 16, 2488, 1331))

    # Set Communication Display Units to Celsius
    SendPacket(BuildModbusPacket(Settings.Address.Value, 16, 2490, 15))

    Off()

def ondisconnect():
    Off()
    TemperatureMonitoring()

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
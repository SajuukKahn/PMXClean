#DisplayName = Get Temperature
#Description = Gets the current temperature
#Icon = ArrowLeftTopMaterialIcon
#SubIcon = ThermometerMaterialIcon

def __inputs__():
    pass

def __run__():
    response = SendAndReceiveTemperature(BuildModbusPacket(3, 360, 2), True)
    if response is None:
        __exceptionhandling__()
    else:
        Outputs.Temperature.Value = float(response)
        SetTemperatureReading(Outputs.Temperature.Value)

def __virtual__():
    pass

def __outputs__():
    #Description = The current temperature
    Outputs.Temperature = new.double(0, -5000, 5000, 0.1, 1, "[Unit]", __source__)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
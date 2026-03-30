#DisplayName = Get Set Point
#Discription = Gets the current set point
#Icon = ArrowLeftTopMaterialIcon
#SubIcon = FireMaterialIcon

def __inputs__():
    pass

def __run__():
    response = SendAndReceiveTemperature(BuildModbusPacket(3, 2160, 2), True)
    if response is None:
        __exceptionhandling__()
    else:
        Outputs.SetPoint.Value = float(response)

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Set Point
    #Description = The current set point
    Outputs.SetPoint = new.double(0, -5000, 5000, 0.1, 1, "[Unit]", __source__)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
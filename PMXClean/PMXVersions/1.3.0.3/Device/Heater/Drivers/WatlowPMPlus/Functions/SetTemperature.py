#DisplayName = Set Temperature
#Description = Sets the desired temperature for the heater
#Icon = ArrowRightTopMaterialIcon
#SubIcon = ThermometerMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

def __inputs__():
    #DisplayName = Set Point
    #Description = The desired temperature
    Inputs.SetPoint = new.double(0, 0, 100, 0.1, 1, "[Unit]", __source__)

def __run__():
    SendPacket(BuildModbusPacket(16, 2160, float(Inputs.SetPoint.Value)))
    On()
    Outputs.SetPoint.Value = Inputs.SetPoint.Value
    UpdateSetPoint(Inputs.SetPoint.Value)

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Set Point
    #Description = The desired temperature
    Outputs.SetPoint = new.double(0, 0, 70, 0.1, 1, "[Unit]", __source__)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
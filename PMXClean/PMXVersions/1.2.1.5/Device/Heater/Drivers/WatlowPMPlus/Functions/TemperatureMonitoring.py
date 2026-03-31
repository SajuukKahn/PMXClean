#DisplayName = Temperature Monitoring
#Description = Monitors for a critical over temperature
#Icon = ThermometerLinesMaterialIcon
#Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    SetUnitsFromDevice(BuildModbusPacket(Settings.Address.Value, 3, 1838, 1))

    if AnalogInputError():
        __throwexception__(Exceptions.AnalogInputError, 0.0)
        return

    Outputs.Temperature.Value = GetTemperature().Temperature.Value
    Outputs.SetPoint.Value = GetSetPoint().SetPoint.Value
    Outputs.IsControlLoopOn.Value = GetIsOn()

    if (Outputs.Temperature.Value >= Settings.CriticalOverTemp.Value) or ((Settings.OverTempInput is not None) and (Settings.OverTempInput.Value == Settings.OverTempState.Value)):
        Outputs.IsOverTemp.Value = True
        __throwexception__(Exceptions.CriticalOvertempReached, Outputs.Temperature.Value)
    else:
        Outputs.IsOverTemp.Value = False

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #Description = The current temperature
    Outputs.Temperature = new.double(0, -5000, 5000, 0.1, 1, "[Unit]", __source__)

    #Property = True
    #DisplayName = Set Point
    #Description = The desired setpoint
    Outputs.SetPoint = new.double(0, -5000, 5000, 0.1, 1, "[Unit]", __source__)

    #Property = True
    #DisplayName = Control Loop On
    #Description = Is the control loop on
    Outputs.IsControlLoopOn = new.bool(False)

    #Property = True
    #DisplayName = Critical Overtemperature Reached
    #Description = A value indicating the polled state of the exhaust switch
    Outputs.IsOverTemp = new.bool(False)

def __exceptions__():
    Exceptions.CriticalOvertempReached = new.exception("#Heater.Exceptions.Title", "#Heater.Exceptions.CriticalOvertempReached", new.enum("Severity", "Critical").Value, None)
    Exceptions.AnalogInputError = new.exception("#Heater.Exceptions.Title", "#Heater.Exceptions.AnalogInputError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, currentTemp):
    __exceptionhandling__()
    units = GetTemperatureUnits()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), '{:.2f}'.format(currentTemp) + units, '{:.2f}'.format(Settings.CriticalOverTemp.Value) + units])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
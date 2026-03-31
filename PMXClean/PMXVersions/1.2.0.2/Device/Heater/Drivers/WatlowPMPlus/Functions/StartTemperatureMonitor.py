#DisplayName = Start Temperature Monitoring
#Description = Start Monitoring the heater to ensure temperature stays within a given range
#Icon = ThermometerMaterialIcon
#SubIcon = PlayMaterialIcon
#Flags = IsProcessStep, IsTriggerStep, IsHidden

def __inputs__():
    #DisplayName = Desired Temperature
    #Description = The desired temperature that must be maintained
    #CanReference = True
    Inputs.DesiredTemperature = new.double(0, 0, 70, 0.1, 1, "[Unit]", __source__)

    #Description = The temperature deviation that will be allowed
    Inputs.Deviation = new.double(0, 0, 100, 0.1, 1, "%")

    #DisplayName = Wait for Temperature
    #Description = A value indicating whether to wait for temperature if current temperature is lower than desired temperature - deviation
    Inputs.WaitForTemperature = new.bool(False)

def __run__():
    allowedLow = GetDeviationLow(ConvertUnits(Inputs.DesiredTemperature.Value), Inputs.Deviation.Value)

    if (Inputs.WaitForTemperature.Value) and (ConvertUnits(GetTemperature().Temperature.Value) < allowedLow):
        WaitForTemp(new.double(ConvertBack(allowedLow)))

    PVA.Heaters.StartTemperatureMonitoring(GetDeviceParameter(), Inputs.DesiredTemperature.Value, Inputs.Deviation.Value, StopTemperatureMonitor.Target)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
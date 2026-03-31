#DisplayName = Stop Temperature Monitoring
#Description = Stop Monitoring the Heater and throw any errors that were not thrown immediately
#Icon = ThermometerMaterialIcon
#SubIcon = StopMaterialIcon
#Flags = IsProcessStep, IsTriggerStep, IsHidden

def __inputs__():
    pass

def __run__():
    error = PVA.Heaters.StopTemperatureMonitoring(GetDeviceParameter())
    if error is not None:
        if hasattr(error, "High"):
            Exceptions.HeatHigh.ExceptionData.MessageParams = tuple([GetDisplayName(), error.Temperature, error.High, GetTemperatureUnits()])
            PVA.Exceptions.ThrowExceptionAsync(Exceptions.HeatHigh)
        elif hasattr(error, "Low"):
            Exceptions.HeatLow.ExceptionData.MessageParams = tuple([GetDisplayName(), error.Temperature, error.Low, GetTemperatureUnits()])
            PVA.Exceptions.ThrowExceptionAsync(Exceptions.HeatLow)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.HeatLow = new.exception("#Heater.Exceptions.TemperatureOutOfRangeTitle", "#Heater.Exceptions.TemperatureTooLow: {0}\r\n\r\n#Heater.Temperature: {1:N2}{3}\r\n#UI.Minimum: {2:N2}{3}", new.enum("Severity", "Error").Value, None)
    Exceptions.HeatHigh = new.exception("#Heater.Exceptions.TemperatureOutOfRangeTitle", "#Heater.Exceptions.TemperatureTooHigh: {0}\r\n\r\n#Heater.Temperature: {1:N2}{3}\r\n#UI.Maximum: {2:N2}{3}", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, temperature, limit):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), temperature, limit, GetTemperatureUnits()])
    PVA.Exceptions.ThrowExceptionAsync(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
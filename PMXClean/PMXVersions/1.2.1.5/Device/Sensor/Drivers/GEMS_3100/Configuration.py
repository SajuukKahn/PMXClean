def __settings__():
    Settings.Analog = new.analoginput()
    
    #Optional = True
    #DisplayName = Analog Output
    Settings.AnalogOutput = new.analogoutput()

    #Hidden = True
    #DisplayName = Critical Over Pressure
    Settings.CriticalOverPressure = new.double(32747, -1000000, 1000000, 0.1, 1, "[Unit]", __source__)
    Settings.CriticalOverPressure.DisableUnitProviderMinMax = True

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
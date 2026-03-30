# Pressure Range: 0 - 50 bar
# Output: 0.5 - 3.0 VDC
# Over Pressure: 150 bar

def __settings__():
    Settings.Analog = new.analoginput()

    #Optional = True
    Settings.Output = new.output()

    #Hidden = True
    #DisplayName = Critical Over Pressure
    Settings.CriticalOverPressure = new.double(2175.57, -1000000, 1000000, 0.1, 1, "[Unit]", __source__)
    Settings.CriticalOverPressure.DisableUnitProviderMinMax = True

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
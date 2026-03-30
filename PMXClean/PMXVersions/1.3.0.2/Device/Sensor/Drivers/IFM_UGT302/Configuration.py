def __settings__():
    Settings.Analog = new.analoginput()

    #DisplayName = Debounce Time
    Settings.DebounceTime = new.int(50, 0, 1000, 5, 10, "ms")

    #Private = True
    #DisplayName = Use Fail Safe
    #Description = If enabled, the sensor will also give "Low" feedback when out of a range from pre-defined fail-safe tolerances.
    Settings.UseFailSafe = new.bool(True)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
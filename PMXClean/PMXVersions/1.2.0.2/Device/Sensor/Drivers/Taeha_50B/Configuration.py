# Pressure Range: 0 - 50 bar
# Output: 0.5 - 3.0 VDC
# Over Pressure: 150 bar

def __settings__():
    Settings.Analog = new.analoginput()

    #Optional = True
    Settings.Output = new.output()

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
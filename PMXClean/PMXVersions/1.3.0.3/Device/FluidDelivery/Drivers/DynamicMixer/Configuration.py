def __settings__():
    #DisplayName = Mixer Axis
    #Description = The axis driving this dynamic mixer
    Settings.MixerAxis = new.axis("Controller0")

    #Description = The conversion rate to set the dispense rate in RPM
    #Private = True
    Settings.Conversion = new.double(66.6667, 1, 999999999, 1, 10, "")

    #Optional = True
    #DisplayName = Mixer in Place Sensor
    #Description = The sensor that checks if the static mixer is present
    Settings.MixerInPlaceSensor = new.device("Proximity", 0)

def ready():
    pass

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
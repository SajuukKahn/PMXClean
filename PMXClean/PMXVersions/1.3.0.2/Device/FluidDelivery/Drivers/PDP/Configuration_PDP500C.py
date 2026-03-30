# Pump Axis Values
# AC/DC = 9999999
# FL = MaxInt, BL = MinInt
# MT = -1, CE = 2
# errorLimit = 2000
# torqueLimit = 9.9
# speed limit = 311296 cnts/sec
# KD = 161.13, KP = 20.63, KI = 0.69

def __settings__():
    #DisplayName = Pump A Axis
    #RetainValue = True
    Settings.PumpAAxis = new.axis("Controller0")

    #DisplayName = Pump B Axis
    #RetainValue = True
    Settings.PumpBAxis = new.axis("Controller0")

    #DisplayName = Minimum Rate
    #Private = True
    Settings.MinimumRate = new.double(0.5, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Maximum Rate
    #Private = True
    Settings.MaximumRate = new.double(5.0, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Pump A Nominal Displacement
    #Private = True
    Settings.NominalDisplacementA = new.double(0.36874, 0, 10000, 0.01, 0.1, "mL/rev")

    #DisplayName = Pump B Nominal Displacement
    #Private = True
    Settings.NominalDisplacementB = new.double(0.36874, 0, 10000, 0.01, 0.1, "mL/rev")

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
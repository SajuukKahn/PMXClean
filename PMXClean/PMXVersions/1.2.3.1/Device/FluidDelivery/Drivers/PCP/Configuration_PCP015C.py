# Pump Axis Values
# AC/DC = 9999999
# FL = MaxInt, BL = MinInt
# MT = -1, CE = 2
# errorLimit = 2000
# torqueLimit = 9.9
# speed limit = 253952 cnts/sec
# KD = 161.13, KP = 20.63, KI = 0.69

def __settings__():
    #DisplayName = Pump Axis
    Settings.PumpAAxis = new.axis("Controller0")

    #DisplayName = Minimum Rate
    #Private = True
    Settings.MinimumRate = new.double(0.015, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Maximum Rate
    #Private = True
    Settings.MaximumRate = new.double(0.15, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Counts Per Rev
    #Private = True
    Settings.PumpACountsPerRev = new.int(126277, 1000, 500000, 100, 1000, "counts/rev")

    #DisplayName = Calibration
    #Private = True
    Settings.PumpACalibration = new.int(207477, 0, 999999, 10, 100, "counts/sec for 1 mL/min")

    #DisplayName = Nominal Displacement
    #Private = True
    Settings.NominalDisplacementA = new.double(0.0102, 0, 10000, 0.5, 1, "mL/rev")

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
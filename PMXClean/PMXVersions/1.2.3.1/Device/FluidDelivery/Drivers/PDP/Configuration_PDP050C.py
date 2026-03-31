# Pump Axis Values
# AC/DC = 9999999
# FL = MaxInt, BL = MinInt
# MT = -1, CE = 2
# errorLimit = 2000
# torqueLimit = 9.9
# speed limit = 253952 cnts/sec
# KD = 161.13, KP = 20.63, KI = 0.69

def __settings__():
    #DisplayName = Pump A Axis
    Settings.PumpAAxis = new.axis("Controller0")

    #DisplayName = Pump B Axis
    Settings.PumpBAxis = new.axis("Controller0")

    #DisplayName = Minimum Rate
    #Private = True
    Settings.MinimumRate = new.double(0.05, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Maximum Rate
    #Private = True
    Settings.MaximumRate = new.double(0.5, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Pump A Counts Per Rev
    #Private = True
    Settings.PumpACountsPerRev = new.int(126277, 1000, 500000, 100, 1000, "counts/rev")

    #DisplayName = Pump B Counts Per Rev
    #Private = True
    Settings.PumpBCountsPerRev = new.int(126277, 1000, 500000, 100, 1000, "counts/rev")

    #DisplayName = Pump A Calibration
    #Private = True
    Settings.PumpACalibration = new.int(52513, 0, 999999, 10, 100, "counts/sec for 1 mL/min")

    #DisplayName = Pump B Calibration
    #Private = True
    Settings.PumpBCalibration = new.int(52513, 0, 999999, 10, 100, "counts/sec for 1 mL/min")

    #DisplayName = Pump A Nominal Displacement
    #Private = True
    Settings.NominalDisplacementA = new.double(0.0403, 0, 10000, 0.01, 0.1, "mL/rev")

    #DisplayName = Pump B Nominal Displacement
    #Private = True
    Settings.NominalDisplacementB = new.double(0.0403, 0, 10000, 0.01, 0.1, "mL/rev")

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
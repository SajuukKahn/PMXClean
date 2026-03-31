#  - - - - - - - - - Common Pump Max Values - - - - - - - - - -
#    Carbide pumps with thermal interface material should be limited to 10 RPM
#    ALL OTHER PUMPS HAVE A 100 RPM Max Speed
#
# PCP015: 126277 counts/rev
#   Critical Overpressure : 2.0 MPa (~290 psi)
#   SUS303 (Stainless Steel) Rotor
#      0.0170 mL/rev nominal displacement
#      124486 counts/sec for 1 mL/min
#      253952 cnts/sec Max Motor Speed
#      0.015 - 1.8 mL/min Dispense Rate
#   Carbide Rotor
#      0.0102 mL/rev nominal displacement
#      207477 counts/sec for 1 mL/min
#      253952 cnts/sec Max Motor Speed
#      0.015 - 0.15 mL/min Dispense Rate
#
# PCP050: 126277 counts/rev
#   Critical Overpressure : 2.0 MPa (~290 psi)
#   SUS303 (Stainless Steel) Rotor
#      0.0490 mL/rev nominal displacement
#      43189 counts/sec for 1 mL/min
#      253952 cnts/sec Max Motor Speed
#      0.05 - 6 mL/min Dispense Rate
#   Carbide Rotor
#      0.0403 mL/rev nominal displacement
#      52513 counts/sec for 1 mL/min
#      253952 cnts/sec Max Motor Speed
#      0.05 - 0.5 mL/min Dispense Rate
#
# PCP150: 155520 counts/rev
#   Critical Overpressure : 2.0 MPa (~290 psi)
#   SUS303 (Stainless Steel) Rotor
#      0.1700 mL/rev nominal displacement
#      15230 counts/sec for 1 mL/min
#      311296 cnts/sec Max Motor Speed
#      0.15 - 18 mL/min Dispense Rate
#   Carbide Rotor
#      0.1713 mL/rev nominal displacement
#      15144 counts/sec for 1 mL/min
#      311296 cnts/sec Max Motor Speed
#      0.15 - 1.5 mL/min Dispense Rate
#
# PCP500: 155520 counts/rev
#   Critical Overpressure : 1.0 MPa (~145 psi)
#   SUS303 (Stainless Steel) Rotor
#      0.4500 mL/rev nominal displacement
#      5765 counts/sec for 1 mL/min
#      311296 cnts/sec Max Motor Speed
#      0.5 - 60 mL/min Dispense Rate
#   Carbide Rotor
#      0.3905 mL/rev nominal displacement
#      6643 counts/sec for 1 mL/min
#      311296 cnts/sec Max Motor Speed
#      0.5 - 5 mL/min Dispense Rate
#
# PCP1000: 155520 counts/rev
#   SUS303 (Stainless Steel) Rotor
#      1.1000 mL/rev
#      2358 counts/sec for 1 mL/min
#      311296 cnts/sec Max Motor Speed
#      1 - 120 mL/min Dispense Rate
#   Carbide Rotor
#      0.8608 mL/rev
#      3014 counts/sec for 1 mL/min
#      311296 cnts/sec Max Motor Speed
#      1 - 10 mL/min Dispense Rate
#
# AC/DC = 9999999
# FL = MaxInt, BL = MinInt
# MT = -1, CE = 2
# errorLimit = 2000
# torqueLimit = 9.9
# speed limit = 253952-311296 cnts/sec
# KD = 161.13, KP = 20.63, KI = 0.69

def __settings__():
    #DisplayName = Pump Axis
    Settings.PumpAAxis = new.axis("Controller0", 0)

    #DisplayName = Minimum Rate
    Settings.MinimumRate = new.double(0.015, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Maximum Rate
    Settings.MaximumRate = new.double(1.8, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Counts Per Rev
    Settings.PumpACountsPerRev = new.int(126277, 1000, 500000, 100, 1000, "counts/rev")

    #DisplayName = Calibration
    Settings.PumpACalibration = new.int(124486, 0, 999999, 10, 100, "counts/sec for 1 mL/min")

    #DisplayName = Nominal Displacement
    Settings.NominalDisplacementA = new.double(0.0170, 0, 10000, 0.5, 1, "mL/rev")

def ready():
    axis = GetPumpAAxis()
    if axis is None:
        __throwexception__(Exceptions.AxisMissing)
        return

    if (axis.Speed > axis.SpeedLimit):
        __throwexception__(Exceptions.PumpSpeedHigh)

def __exceptions__():
    Exceptions.AxisMissing = new.exception("#FluidDelivery.Exceptions.AxisMissingTitle", "#FluidDelivery.Exceptions.AxisMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.PumpSpeedHigh = new.exception("#FluidDelivery.Exceptions.FluidDeliveryExceptionTitle", "#FluidDelivery.Exceptions.DispenseRateHigh", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
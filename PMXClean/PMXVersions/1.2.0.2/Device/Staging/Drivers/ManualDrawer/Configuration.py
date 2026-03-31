def __settings__():
    #Optional = True
    #DisplayName = Part Sensors
    #Description = The optional sensor that must be on for the code execution to continue
    Settings.PartSensors = new.devicelist("PIP", 0)

    #DisplayName = Interior Lock
    #Description = The pnumatic lock for the retracted position
    Settings.InteriorLock = new.device("Lock", 0)

    #DisplayName = Exterior Lock
    #Description = The pnumatic lock for the extended position
    Settings.ExteriorLock = new.device("Lock", 1)

    #DisplayName = Fully Retracted
    #Description = The sensor to tell if the drawer is fully retracted
    Settings.FullyRetracted = new.device("Proximity", 0)

    #DisplayName = Fully Extended
    #Description = The sensor to tell if the drawer is fully extended
    Settings.FullyExtended = new.device("Proximity", 1)

    #DisplayName = Gantry Power
    #Description = The gantry power input
    Settings.GantryPower = new.input()

    #DisplayName = Gantry Power On State
    #Description = The state of the gantry power input when gantry power is on
    Settings.GantryPowerOnState = new.bool()

    #Optional = True
    #DisplayName = Cycle Start
    #Description = The cycle start input that must be in the defined On State to continue code execution
    Settings.CycleStart = new.input()

    #DisplayName = Cycle Start On State
    #Description = A value indicating the required input state of the Cycle Start input in order to be considered On
    Settings.CycleStartOnState = new.bool(False, True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
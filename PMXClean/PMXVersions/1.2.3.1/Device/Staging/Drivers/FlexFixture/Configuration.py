def __settings__():
    #Optional = True
    #Enabled = False
    #DisplayName = Part Sensors
    #Description = The optional sensor that must be on for the code execution to continue
    Settings.PartSensor = new.device("PIP", 0)

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
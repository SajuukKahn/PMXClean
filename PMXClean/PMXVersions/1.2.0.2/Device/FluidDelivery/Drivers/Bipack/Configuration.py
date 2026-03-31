def __settings__():
    #Reserved = true
    #DisplayName = Dispense Air Pressure
    Settings.DispenseAirOutput = new.output()

    #Reserved = true
    #DisplayName = Refill Air Output
    Settings.RefillAirOutput = new.output()

def ready():
    On()

def complete():
    Off()

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
def __settings__():
    Settings.Output = new.output()

    #DisplayName = Extended Input
    Settings.ExtendedInput = new.input()

    #DisplayName = Retracted Input
    Settings.RetractedInput = new.input()

    #DisplayName = Locked State
    Settings.LockedState = new.bool(True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
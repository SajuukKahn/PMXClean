def __settings__():
    #DisplayName = Enable Output
    Settings.EnableOutput = new.output()

    #DisplayName = Direction Output
    Settings.DirectionOutput = new.output()

    #DisplayName = Forward State
    Settings.ForwardState = new.bool(False, True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
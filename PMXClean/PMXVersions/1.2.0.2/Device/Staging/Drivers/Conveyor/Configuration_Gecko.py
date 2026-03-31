def __settings__():
    #DisplayName = Enable Output
    Settings.EnableOutput = new.output()

    #DisplayName = Left Direction Output
    Settings.LeftDirectionOutput = new.output()

    #DisplayName = Left Forward State
    Settings.LeftForwardState = new.bool(True, True)

    #DisplayName = Right Direction Output
    Settings.RightDirectionOutput = new.output()

    #DisplayName = Right Forward State
    Settings.RightForwardState = new.bool(False, True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
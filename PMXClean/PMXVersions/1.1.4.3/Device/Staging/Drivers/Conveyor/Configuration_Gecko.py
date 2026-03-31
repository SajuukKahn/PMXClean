def __settings__():
    Settings.EnableOutput = new.output()
    Settings.LeftDirectionOutput = new.output()
    Settings.LeftForwardState = new.bool(True, True)
    Settings.RightDirectionOutput = new.output()
    Settings.RightForwardState = new.bool(False, True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
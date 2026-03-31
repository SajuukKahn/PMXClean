def __settings__():
    Settings.PositionAOutput = new.output()
    Settings.PositionBOutput = new.output()
    Settings.PositionAInput = new.input()
    Settings.PositionBInput = new.input()
    Settings.ActuatedAState = new.bool(True)
    Settings.ActuatedBState = new.bool(True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
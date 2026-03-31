def __settings__():
    #DisplayName = Position A Output
    Settings.PositionAOutput = new.output()

    #DisplayName = Position B Output
    Settings.PositionBOutput = new.output()

    #DisplayName = Position A Input
    Settings.PositionAInput = new.input()

    #DisplayName = Position B Input
    Settings.PositionBInput = new.input()

    #DisplayName = Actuated A State
    Settings.ActuatedAState = new.bool(True)

    #DisplayName = Actuated B State
    Settings.ActuatedBState = new.bool(True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
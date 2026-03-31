def __settings__():
    Settings.Output = new.output()

    #DisplayName = Left Input
    Settings.LeftInput = new.input()

    #DisplayName = Right Input
    Settings.RightInput = new.input()

    #DisplayName = Actuated State
    Settings.ActuatedState = new.bool(True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
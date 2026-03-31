def __settings__():
    Settings.Output = new.output()

    #DisplayName = Front Input
    Settings.FrontInput = new.input()

    #DisplayName = Rear Input
    Settings.RearInput = new.input()

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
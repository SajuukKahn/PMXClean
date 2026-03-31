def __settings__():
    Settings.Output= new.output()

    #DisplayName = Up Input
    Settings.UpInput = new.input()

    #DisplayName = Down Input
    Settings.DownInput = new.input()

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
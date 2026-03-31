def __settings__():
    Settings.Output = new.output()

    #DisplayName = On Input
    Settings.OnInput = new.input()

    #DisplayName = Shutter Input
    Settings.ShutterInput = new.input()

    #DisplayName = Shutter Open State
    Settings.ShutterOpenState = new.bool(True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
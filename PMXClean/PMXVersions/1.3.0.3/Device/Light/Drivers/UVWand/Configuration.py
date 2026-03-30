def __settings__():
    #DisplayName = Shutter Output
    Settings.Output = new.output()

    #DisplayName = Lamp On Input
    Settings.OnInput = new.input()

    #DisplayName = Shutter Input
    Settings.ShutterInput = new.input()

    #DisplayName = Shutter Open State
    Settings.ShutterOpenState = new.bool(True)

    #DisplayName = Handshake Option
    Settings.HandshakeOption = new.enum(["Latching", "Toggle"],"Latching")

def ready():
    On()

def complete():
    Off()

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
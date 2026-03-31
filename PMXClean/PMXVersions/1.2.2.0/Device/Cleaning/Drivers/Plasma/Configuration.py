def __settings__():
    #DisplayName = Generator On
    Settings.GeneratorOn = new.output()

    #DisplayName = On Output
    Settings.OnOutput = new.output()

    #Optional = True
    #DisplayName = Fault Reset
    Settings.FaultReset = new.output()

    #Optional = True
    #DisplayName = Control Relay
    Settings.ControlRelay = new.output()

    Settings.Fault = new.input()
    Settings.Ready = new.input()

    #DisplayName = On Input
    Settings.OnInput = new.input()

    #DisplayName = Fault State
    Settings.FaultState = new.bool(False)

    #DisplayName = Ready State
    Settings.ReadyState = new.bool(True)

    #DisplayName = On State
    Settings.OnState = new.bool(True)

def ready():
    On()

def complete():
    Off()

def __exceptions__():
    pass
def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
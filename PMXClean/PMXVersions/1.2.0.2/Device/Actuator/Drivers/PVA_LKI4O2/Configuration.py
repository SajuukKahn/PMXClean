def __settings__():
    #DisplayName = Lock Output
    Settings.LockOutput = new.output()

    #DisplayName = Unlock Output
    Settings.UnlockOutput = new.output()

    #DisplayName = Lock A Extended
    Settings.LockAExtended = new.input()

    #DisplayName = Lock A Retracted
    Settings.LockARetracted = new.input()

    #DisplayName = Lock B Extended
    Settings.LockBExtended = new.input()

    #DisplayName = Lock B Retracted
    Settings.LockBRetracted = new.input()

    #DisplayName = Locked State
    Settings.LockedState = new.bool(True)

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
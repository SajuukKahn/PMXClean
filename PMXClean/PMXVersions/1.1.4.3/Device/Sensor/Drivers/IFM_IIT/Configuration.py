def __settings__():
    Settings.Input = new.input()
    Settings.OnState = new.bool(False, True)
    Settings.DebounceTime = new.int(50, 0, 1000, 5, 10, "ms")

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
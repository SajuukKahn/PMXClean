def __settings__():
    Settings.Input = new.input()
    
    #DisplayName = On State
    Settings.OnState = new.bool(False, True)

    #DisplayName = Debounce Time
    Settings.DebounceTime = new.int(50, 0, 1000, 5, 10, "ms")

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
def __settings__():
    #DisplayName = Red Output
    Settings.RedOutput = new.output()

    #DisplayName = Amber Output
    Settings.AmberOutput = new.output()

    #DisplayName = Green Output
    Settings.GreenOutput = new.output()

    #DisplayName = Alarm Output
    Settings.AlarmOutput = new.output()

    #DisplayName = Flash Wait
    Settings.FlashWait = new.int(750, 0, 5000, 1, 10, "ms")

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
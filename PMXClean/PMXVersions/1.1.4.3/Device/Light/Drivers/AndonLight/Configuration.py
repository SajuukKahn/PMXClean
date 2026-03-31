def __settings__():
    Settings.RedOutput = new.output()
    Settings.AmberOutput = new.output()
    Settings.GreenOutput = new.output()
    Settings.AlarmOutput = new.output()
    Settings.FlashWait = new.int(0, 0, 2000, 1, 10, "ms")

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
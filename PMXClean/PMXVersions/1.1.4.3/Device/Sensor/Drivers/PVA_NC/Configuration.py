def __settings__():
    Settings.XSensor = new.input()
    Settings.YSensor = new.input()
    Settings.ZSensor = new.input()
    Settings.XSensorOnState = new.bool(False, True)
    Settings.YSensorOnState = new.bool(False, True)
    Settings.ZSensorOnState = new.bool(False, True)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
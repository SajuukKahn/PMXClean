def __settings__():
    #DisplayName = X Sensor
    Settings.XSensor = new.input()

    #DisplayName = Y Sensor
    Settings.YSensor = new.input()

    #DisplayName = Z Sensor
    Settings.ZSensor = new.input()

    #DisplayName = X Sensor On State
    Settings.XSensorOnState = new.bool(False, True)

    #DisplayName = Y Sensor On State
    Settings.YSensorOnState = new.bool(False, True)

    #DisplayName = Z Sensor On State
    Settings.ZSensorOnState = new.bool(False, True)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
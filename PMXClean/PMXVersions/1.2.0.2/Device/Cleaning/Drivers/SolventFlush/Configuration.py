def __settings__():
    #DisplayName = Flush Output
    #Description = The output that flushes the system.
    Settings.FlushOutput = new.output()

    #DisplayName = Cup Sensors
    #Description = The sensors that detect when a cup has an obstruction.
    Settings.CupSensors = new.devicelist("Low Level")

    #DisplayName = Bottle Sensors
    #Description = The sensors that detect when a bottle is full.
    Settings.BottleSensors = new.devicelist("Low Level")

    #DisplayName = Manual Flush Time
    #Description = The amount of time to flush the system for during manual operation.
    Settings.ManualFlushTime = new.double(2, .1, 15, .1, 1, "s")

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
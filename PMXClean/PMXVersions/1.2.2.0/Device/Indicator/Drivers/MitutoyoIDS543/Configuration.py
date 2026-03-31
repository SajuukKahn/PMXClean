import time

def __settings__():
    #Private = True
    #DisplayName = Relative Calibration Distance
    #Description = The additional distance to descend when calibrating to ensure the device has a valid reading
    Settings.RelativeCalibrationDistance = new.double(6.0, 0.00, 12.7, 0.01, 1.0, "mm")

def onconnect():
    SendPacket("R")
    time.sleep(1.5)
    SendPacket("R")
    response = ReceiveResponse()
    if response is None:
        raise

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
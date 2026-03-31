# DisplayName = Wait For Pressure
# Description = Wait for a specified pressure to be reached
# Icon = ProgressClockMaterialIcon
# Flags = IsProcessStep, IsProgramStep, IsHidden

def __inputs__():
    #Description = The pressure minimum to wait for
    Inputs.Minimum = new.double(0, -32748, 32747, 0.1, 1, "[Unit]", __source__)

    #Description = The maximum amount of time to wait for the pressure to be achieved
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    atpressure = False
    timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
    while not atpressure:
        pressure = GetPressureData().Reading.Value
        atpressure = pressure >= Inputs.Minimum.Value
        if PVA.System.GetCurrentTime().Value > timeout:
            break
        PVA.System.Wait(10)

    if not atpressure:
        __throwexception__(Exceptions.Timeout)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#Sensor.Exceptions.PressureTimeout", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
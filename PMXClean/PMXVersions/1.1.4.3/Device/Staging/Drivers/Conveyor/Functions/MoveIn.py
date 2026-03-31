# DisplayName = Move In
# Description = Moves a part to the indicated PIP sensor by adding one tenant to the schedule, optionally moving the board stop down, with a timeout and an off delay before removing the tenant from the schedule
# Icon = ArrowCollapseRightMaterialIcon
# Flags = IsProcessStep

def __inputs__():
    #Description = The PIP sensor to attempt to activate
    Inputs.Sensor = new.device("PIP", 0)

    #Optional = True
    #DisplayName = Board Stop
    #Description = The Board Stop that will be actuated into the down state
    Inputs.BoardStop = new.device("Board Stop", -1)

    #Description = A value indicating whether to reverse the conveyor direction
    Inputs.Reverse = new.bool(False)

    #Description = The time alloted for the PIP to remain off before throwing an exception
    Inputs.Timeout = new.int(10000, 0, 1000000, 10, 100, "ms")
    
    #DisplayName = Off Delay
    #Description = The time to let the conveyor continue running before turning off, used for handing off between scripts
    Inputs.OffDelay = new.int(200, 0, 2000, 10, 100, "ms")

def __run__():
    if Inputs.Sensor is None:
        __throwexception__(Exceptions.NoSensor)

    ScheduleOn(Inputs.Reverse)
    if Inputs.BoardStop is not None:
        Inputs.BoardStop.Down()
        Inputs.BoardStop.DownCheck(new.int(1000))
    Inputs.Sensor.WaitUntilOn(Inputs.Timeout)
    ScheduleOff(Inputs.OffDelay)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.NoSensor = new.exception("#Sensor.Exceptions.SensorMissingTitle", "#Sensor.Exceptions.SensorMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    Off()

def __exceptionrecovery__():
    pass
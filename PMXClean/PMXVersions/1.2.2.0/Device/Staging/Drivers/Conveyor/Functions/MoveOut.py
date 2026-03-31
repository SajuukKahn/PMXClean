#DisplayName = Move Out
#Description = Moves a part off the indicated PIP sensor by adding one tenant to the schedule, optionally moving the board stop up, with a timeout and an off delay before removing the tenant from the schedule
#Icon = ArrowExpandRightMaterialIcon
#Flags = IsProcessStep

def __inputs__():
    #Optional = True
    #Description = The PIP sensor to attempt to deactivate (if omitted the script turns on the conveyor for the OffDelay value)
    Inputs.Sensor = new.device("PIP", 0)

    #Optional = True
    #DisplayName = Board Stop
    #Description = The Board Stop that will be actuated into the up state
    Inputs.BoardStop = new.device("Board Stop", -1)

    #Description = A value indicating whether to reverse the conveyor direction
    Inputs.Reverse = new.bool(False)

    #Description = The time alloted for the PIP to remain on before throwing an exception
    Inputs.Timeout = new.int(10000, 0, 1000000, 10, 100, "ms")
    
    #DisplayName = Off Delay
    #Description = The time to let the conveyor continue running before turning off, used for handing off between scripts
    Inputs.OffDelay = new.int(200, 0, 20000, 10, 100, "ms")

def __run__():
    if Inputs.BoardStop is not None:
        Inputs.BoardStop.Up()
        Inputs.BoardStop.UpCheck(new.int(1000))
    currentTime = PVA.System.GetCurrentTime().Value

    if Inputs.Sensor is not None:
        while not Inputs.Sensor._PollState_.IsSettled.Value:
            PVA.System.Wait(10)
            if ((currentTime + Inputs.Timeout.Value) < PVA.System.GetCurrentTime()):
                __throwexception__(Exceptions.PIPFlicker)

        sensorState = Inputs.Sensor.CheckState()
        if not sensorState.State.Value:
            return

    ScheduleOn(Inputs.Reverse)
    if Inputs.Sensor is not None:
        Inputs.Sensor.WaitUntilOff(Inputs.Timeout)
    ScheduleOff(Inputs.OffDelay)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.PIPFlicker = new.exception("#Staging.Exceptions.PIPNotSettledTitle", "#Staging.Exceptions.PIPNotSettled", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    Off()

def __exceptionrecovery__():
    pass
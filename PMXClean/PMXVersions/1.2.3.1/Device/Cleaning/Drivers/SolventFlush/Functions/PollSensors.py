#DisplayName = Poll Sensors
#Description = Polls the input states of the solvent flush sensors
#Icon = CupWaterMaterialIcon
#SubIcon = RepeatMaterialIcon
#Flags = IsPolling, IsHidden

counter = 0

def __inputs__():
    pass

def __run__():
    global counter

    # Do not throw an exception the first few times through to allow _PollState_.PolledState to be correct on startup
    if counter < 5:
        counter = counter + 1
        return

    for cupSensor in Settings.CupSensors:
        if hasattr(cupSensor, "_PollState_"):
            if cupSensor._PollState_.PolledState.Value:
                __throwexception__(Exceptions.PurgeCupObstruction, cupSensor.GetDisplayName())
                return

    for bottleSensor in Settings.BottleSensors:
        if hasattr(bottleSensor, "_PollState_"):
            if bottleSensor._PollState_.PolledState.Value:
                __throwexception__(Exceptions.SolventReservoirFull, bottleSensor.GetDisplayName())
                return

    for bottleSensor in Settings.LidSensors:
        if hasattr(bottleSensor, "_PollState_"):
            if not bottleSensor._PollState_.PolledState.Value:
                __throwexception__(Exceptions.SolventLidOpen, bottleSensor.GetDisplayName())
                return

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.PurgeCupObstruction = new.exception("#Cleaning.Exceptions.PurgeCupObstructionTitle", "#Cleaning.Exceptions.PurgeCupObstruction", new.enum("Severity", "Error").Value, None)
    Exceptions.SolventReservoirFull = new.exception("#Cleaning.Exceptions.SolventReservoirFullTitle", "#Cleaning.Exceptions.SolventReservoirFull", new.enum("Severity", "Error").Value, None)
    Exceptions.SolventLidOpen = new.exception("#Cleaning.Exceptions.SolventLidOpenTitle", "#Cleaning.Exceptions.SolventLidOpen", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
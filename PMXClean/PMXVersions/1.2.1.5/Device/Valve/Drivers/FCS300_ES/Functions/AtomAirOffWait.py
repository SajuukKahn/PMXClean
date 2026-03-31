#DisplayName = Atom Air Off Wait
#Description = Wait a minimum amount of time before continuing
#Icon = ClockEndMaterialIcon
#SubIcon = SprayValveCustomIcon

def __inputs__():
    pass

def __run__():
    PVA.System.Wait(Settings.AtomAirOffDelay.Value)

def __virtual__():
    PVA.System.Wait(Settings.AtomAirOffDelay.Value)

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
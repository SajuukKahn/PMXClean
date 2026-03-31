#DisplayName = Reset Pendants
#Description = Reset the pendants to their default state for the given page
#Icon = MicrosoftXboxControllerMenuMaterialIcon
#SubIcon = ReplayMaterialIcon
#IconIndex = All
#Flags = IsTriggerStep

def __inputs__():
    pass

def __run__():
    PVA.Pendants.ResetState()

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
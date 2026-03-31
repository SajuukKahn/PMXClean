#DisplayName = Disable Pendants
#Description = Disable all pendants
#Icon = MicrosoftXboxControllerOffMaterialIcon
#Flags = IsTriggerStep

def __inputs__():
    #DisplayName = Set Default as Disabled
    #Description = A value indicating whether this function will set the default state for pendants
    Inputs.SetDefault = new.bool(True)

def __run__():
    PVA.Pendants.Disable(Inputs.SetDefault.Value)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
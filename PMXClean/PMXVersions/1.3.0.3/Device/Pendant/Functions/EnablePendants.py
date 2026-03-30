#DisplayName = Enable Pendants
#Description = Enable all pendants
#Icon = MicrosoftXboxControllerMaterialIcon
#Flags = IsTriggerStep

def __inputs__():
    #DisplayName = Set Default as Enabled
    #Description = A value indicating whether this function will set the default state for pendants
    Inputs.SetDefault = new.bool(True)

def __run__():
    PVA.Pendants.Enable(Inputs.SetDefault.Value)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
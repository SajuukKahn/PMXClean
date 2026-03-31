# DisplayName = Next Profile
# Description = Increment the current selected profile index
# Icon = MicrosoftXboxControllerMaterialIcon
# SubIcon = InformationMaterialIcon
# Flags = IsMappable

def __inputs__():
    #Description = The pendant to change the selected profile on
    Inputs.Pendant = new.device("Pendant", 0)

def __run__():
    if Inputs.Pendant is None:
        GoToNextProfile(False)
        return
    GoToNextProfile(Inputs.Pendant)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
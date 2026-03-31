# DisplayName = Toggle Help
# Description = Toggle the pendant profile mapping on-screen help popup
# Icon = MicrosoftXboxControllerMaterialIcon
# SubIcon = InformationMaterialIcon
# Flags = IsMappable

def __inputs__():
    #Private = True
    #Description = The pendant to get the profile mapping for
    Inputs.Pendant = new.device("Pendant", 0)

def __run__():
    if Inputs.Pendant is None:
        ToggleHelpWindow(False)
        return
    ToggleHelpWindow(Inputs.Pendant)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
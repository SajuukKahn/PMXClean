# DisplayName = Next Analog Stick Mode
# Description = Toggle an analog stick's feedback mode
# Icon = MicrosoftXboxControllerMaterialIcon
# SubIcon = CursorMoveMaterialIcon
# Flags = IsMappable

def __inputs__():
    #Private = True
    #Description = The pendant to toggle the analog stick feedback mode on
    Inputs.Pendant = new.device("Pendant", 0)

    #Description = The index of the analog stick's feedback mode.
    Inputs.Index = new.int(0, 0, 1, 1, 1, "")

def __run__():
    if Inputs.Pendant is None:
        SetNextAnalogFeedbackMode(False, int(Inputs.Index.Value))
        return
    SetNextAnalogFeedbackMode(Inputs.Pendant, int(Inputs.Index.Value))

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
# DisplayName = Set State
# Description = Set the state of the Red, Green, and Blue lights together
# Icon = LedOnMaterialIcon

def __inputs__():
    #Description = A value indicating the desired state of the red light
    Inputs.Red = new.bool(False)

    #Description = A value indicating the desired state of the green light
    Inputs.Green = new.bool(False)

    #Description = A value indicating the desired state of the blue light
    Inputs.Blue = new.bool(False)

def __run__():
    if (Settings.RedOutput is None):
        __throwexception__(Exceptions.OutputMissing, "RedOutput")
        return

    if (Settings.GreenOutput is None):
        __throwexception__(Exceptions.OutputMissing, "GreenOutput")
        return

    if (Settings.BlueOutput is None):
        __throwexception__(Exceptions.OutputMissing, "BlueOutput")
        return

    Settings.RedOutput.Set(bool(Inputs.Red.Value))
    Settings.GreenOutput.Set(bool(Inputs.Green.Value))
    Settings.BlueOutput.Set(bool(Inputs.Blue.Value))

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
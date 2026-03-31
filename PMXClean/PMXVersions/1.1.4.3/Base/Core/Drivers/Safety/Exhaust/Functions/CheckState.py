# DisplayName = Check State
# Description = Check the state of the exhaust switch
# Icon = LedOnMaterialIcon
# Flags = IsHidden

def __inputs__():
    pass

def __run__():
    if (Settings.Input is None):
        Exceptions.InputMissing.ExceptionData.MessageParams = tuple([GetDisplayName()])
        Outputs.State.Value = not Settings.OnState.Value
        Outputs.Thrown.Value = True
        __throwexception__(Exceptions.InputMissing)

    Outputs.Thrown.Value = False
    Outputs.State.Value = Settings.Input.Value == Settings.OnState.Value

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating the state of the exhaust switch
    Outputs.State = new.bool(False)

    #Description = A value indicating whether the check threw an exception
    Outputs.Thrown = new.bool(False)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
# DisplayName = Exhaust Flow Monitor
# Description = Execute a single check as part of the exhaust monitoring loop
# Icon = FanMaterialIcon
# Flags = IsHidden

def __inputs__():
    #DisplayName = Exhaust Switch
    #Description = The exhaust switch to check
    Inputs.ExhaustSwitch = new.device("Exhaust Switch", 0)

def __run__():
    if Inputs.ExhaustSwitch is None:
        Outputs.FanPass.Value = False
        __throwexception__(Exceptions.FanInputRequired)
        return
    
    if not Inputs.ExhaustSwitch.CheckState().State.Value:
        Outputs.FanPass.Value = False
        SetExhaustCheckPassed(False)
        __throwexception__(Exceptions.ExhaustCheckFailure)

    Outputs.FanPass.Value = True

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Fan Pass
    #Description = A value indicating whether the exhaust flow check has been completed successfully
    Outputs.FanPass = new.bool(False)

def __exceptions__():
    Exceptions.FanInputRequired = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ExhaustCheckFailure = new.exception("#Safety.Exceptions.ExhaustFailTitle", "#Safety.Exceptions.ExhaustFail", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

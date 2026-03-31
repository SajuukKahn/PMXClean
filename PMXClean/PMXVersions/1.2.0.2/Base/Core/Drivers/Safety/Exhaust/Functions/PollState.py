#DisplayName = Poll State
#Description = Poll the state of the exhaust switch
#Icon = PollMaterialIcon
#Flags = IsPolling, IsHidden

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    if (PVA.Safety.GetExhaustFlowCheckBypass() is True):
        return

    if (Settings.Input is None):
        Outputs.PolledState.Value = not Settings.OnState.Value
        if thrown:
            return
        thrown = True
        Exceptions.InputMissing.ExceptionData.MessageParams = tuple([GetDisplayName()])
        __throwexception__(Exceptions.InputMissing)
        return
    thrown = False
    Outputs.PolledState.Value = Settings.Input.Value == Settings.OnState.Value

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Polled State
    #Description = A value indicating the polled state of the exhaust switch
    Outputs.PolledState = new.bool(False)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
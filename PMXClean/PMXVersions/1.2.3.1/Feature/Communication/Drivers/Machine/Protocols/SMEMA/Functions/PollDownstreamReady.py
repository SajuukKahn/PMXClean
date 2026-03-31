#DisplayName = Poll Machine Ready
#Description = Poll Downstream ready to receive ready status
#Icon = CableDataMaterialIcon
#SubIcon = ArrowDownMaterialIcon
#Flags = IsPolling

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown

    if Settings.DownstreamReady is None:
        Outputs.Status.Value = not Settings.DownstreamReadyState.Value
        if thrown:
            return None
        thrown = True
        __throwexception__(Exceptions.ConfigValueRequired, "SMEMA Output")
        return
    thrown = False

    Outputs.Status.Value = (Settings.DownstreamReady.Value == Settings.DownstreamReadyState.Value)

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Machine Ready
    #Description = A value indicating the state of downstream machine ready to receive a part
    Outputs.Status = new.bool(False)

def __exceptions__():
    Exceptions.ConfigValueRequired = new.exception("#Scripting.Exceptions.ConfigValueRequiredTitle", "#Scripting.Exceptions.ConfigValueRequired", new.enum("Severity", "Silent").Value, None)
    
def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple(["Get SMEMA", name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
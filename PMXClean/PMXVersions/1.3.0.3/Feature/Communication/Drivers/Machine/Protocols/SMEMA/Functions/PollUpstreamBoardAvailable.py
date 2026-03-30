#DisplayName = Poll Board Available
#Description = Poll Upstream Board Available status
#Icon = CableDataMaterialIcon
#SubIcon = ArrowUpMaterialIcon
#Flags = IsPolling

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    
    if Settings.UpstreamBoardAvailable is None:
        Outputs.Status.Value = not Settings.UpstreamBoardAvailableState.Value
        if thrown:
            return None
        thrown = True
        __throwexception__(Exceptions.ConfigValueRequired, "SMEMA Output")
        return
    thrown = False

    Outputs.Status.Value = (Settings.UpstreamBoardAvailable.Value == Settings.UpstreamBoardAvailableState.Value)

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Board Available
    #Description = A value indicating the state of the upstream machine ready to send a board
    Outputs.Status = new.bool(False, True)

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
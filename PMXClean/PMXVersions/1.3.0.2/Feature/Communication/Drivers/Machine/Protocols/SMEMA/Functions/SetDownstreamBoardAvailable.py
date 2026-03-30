#DisplayName = Set Board Available
#Description = Set Downstream Board Available output to indicate send status
#Icon = CableDataMaterialIcon
#SubIcon = ArrowDownMaterialIcon
#Flags = IsProcessStep, IsTriggerStep

def __inputs__():
    #DisplayName = Set Value
    #Description = The value to set the output to
    Inputs.SetValue = new.bool(True)

def __run__():
    if Settings.DownstreamBoardAvailable is None:
        __throwexception__(Exceptions.ConfigValueRequired, "SMEMA Output")
        return

    Settings.DownstreamBoardAvailable.Set(Inputs.SetValue.Value)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ConfigValueRequired = new.exception("#Scripting.Exceptions.ConfigValueRequiredTitle", "#Scripting.Exceptions.ConfigValueRequired", new.enum("Severity", "Error").Value, None)
    
def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple(["Set SMEMA", name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
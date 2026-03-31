#DisplayName = Down
#Description = Call the "Down" function on a provided tool
#Icon = ArrowDownBoldOutlineMaterialIcon
#SubIcon = DispenseValveBoldCustomIcon
#Flags = IsProgramStep

def __inputs__():
    #Description = The tool to call the function on
    Inputs.Tool = new.tool(0)

def __run__():
    if Inputs.Tool is None:
        __throwexception__(Exceptions.ToolRequired)

    PVA.System.TryExecuteDeviceFunction(Inputs.Tool, "Down")

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ToolRequired = new.exception("#Tool.Exceptions.NoToolTitle", "#Tool.Exceptions.NoTool", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
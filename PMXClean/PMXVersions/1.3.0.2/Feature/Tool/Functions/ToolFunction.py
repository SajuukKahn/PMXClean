#DisplayName = Tool Function
#Description = Call the a function by name on a provided tool
#Icon = HammerWrenchMaterialIcon
#SubIcon = DispenseValveBoldCustomIcon
#Flags = IsProgramStep

def __inputs__():
    #Description = The tool to call the function on
    Inputs.Tool = new.tool(0)
    
    #DisplayName = Function Name
    #Description = The function to attempt to call
    Inputs.FunctionName = new.toolfunction("Up")

def __run__():
    if Inputs.Tool is None:
        __throwexception__(Exceptions.ToolRequired)

    PVA.System.TryExecuteDeviceFunction(Inputs.Tool, Inputs.FunctionName.Value)

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
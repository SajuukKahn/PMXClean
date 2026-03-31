#DisplayName = Set Output
#Description = Change a discrete output state
#Icon = AlarmLightMaterialIcon
#Flags = IsProcessStep, IsTriggerStep

def __inputs__():
    #DisplayName = Output
    #Description = The output to change
    Inputs.Output = new.output()

    #DisplayName = Set Value
    #Description = The value to change the output to
    Inputs.SetValue = new.bool(True)

def __run__():
    if (Inputs.Output is None):
        __throwexception__(Exceptions.OutputMissing, "Output")
        return

    Inputs.Output.Set(Inputs.SetValue.Value)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Scripting.Exceptions.ScriptValueRequired", new.enum("Severity", "Error").Value, None)
    
def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple(["Set Output", name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
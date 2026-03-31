# DisplayName = Set SMEMA
# Description = Change an output state for SMEMA communication
# Icon = CableDataMaterialIcon
# Flags = IsProcessStep, IsTriggerStep

def __inputs__():
    #DisplayName = SMEMA Output
    #Description = The SMEMA output to change
    Inputs.SMEMAOutput = new.output()

    #DisplayName = Set Value
    #Description = The value to change the output to
    Inputs.SetValue = new.bool(True)

def __run__():
    if (Inputs.SMEMAOutput is None):
        __throwexception__(Exceptions.OutputMissing, "Set SMEMA")
        return

    Inputs.SMEMAOutput.Set(Inputs.SetValue.Value)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#Scripting.Exceptions.ScriptValueRequired", new.enum("Severity", "Error").Value, None)
    
def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple(["Set SMEMA", name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
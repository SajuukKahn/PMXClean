#DisplayName = Set Pass / Fail
#Description = Sets the Inspection Pass Output Value
#Icon = ThumbsUpDownMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = True
    #Description = The state to set the Inspection Pass Output Value to
    Inputs.Pass = new.bool(True)

def __run__():
    if Inputs.Pass is None:
        __throwexception__(Exceptions.PassInputMissing)
        return

    SetPassFailInternal(Inputs.Pass)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.PassInputMissing = new.exception("#Inspection.Exceptions.PassInputMissingTitle", "#Inspection.Exceptions.PassInputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetExecutingStepName()])
    if PVA.Inspection.IsDesignTime():
        PVA.Inspection.WarnException(exception)
    else:
        PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = Value in Range
#Description = Determines if a value is within or without the range specified
#Icon = TableMergeCellsMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = True
    Inputs.Scalar = new.double()
    
    #CanReference = True
    #Optional = True
    #DisplayName = Lower Bound
    #Description = The minimal inclusive value of the range of acceptable values
    Inputs.LowerBound = new.double()
    
    #CanReference = True
    #Optional = True
    #DisplayName = Higher Bound
    #Description = The maximum inclusive value of the range of acceptable values
    Inputs.HigherBound = new.double()

def __run__():
    if Inputs.Scalar is None:
        __throwexception__(Exceptions.InputMissing)
        return

    Outputs.InRange.Value = (Inputs.LowerBound is None or (Inputs.LowerBound.Value <= Inputs.Scalar.Value)) and (Inputs.HigherBound is None or (Inputs.Scalar.Value <= Inputs.HigherBound.Value))

def __virtual__():
    pass

def __outputs__():
    #DisplayName = In Range
    #Description = Whether the input value is within the specified range
    Outputs.InRange = new.bool(False, True)

def __exceptions__():
    Exceptions.InputMissing = new.exception("#Inspection.Exceptions.InputMissingTitle", "#Inspection.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

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
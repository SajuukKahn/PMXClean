#DisplayName = Calculate From Points
#Description = Performs calculations given two points. Note: Care must be taken that the source units of all inputs match
#Icon = AbacusMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = True
    Inputs.X1 = new.double()
    
    #CanReference = True
    Inputs.Y1 = new.double()

    #CanReference = True
    Inputs.X2 = new.double()

    #CanReference = True
    Inputs.Y2 = new.double()

    #Description = The context in which to perform the calculations
    Inputs.Context = new.enum("CalculationContext", "Line")

def __run__():
    CalculateInternal(Inputs.X1, Inputs.Y1, Inputs.X2, Inputs.Y2, Inputs.Context.Value, Outputs.Width, Outputs.Height, Outputs.Length, Outputs.Slope, Outputs.Intercept, Outputs.Perimeter, Outputs.Area)

def __virtual__():
    pass

def __outputs__():
    Outputs.Width = new.double()
    Outputs.Height = new.double()
    Outputs.Length = new.double()
    Outputs.Slope = new.double()
    Outputs.Intercept = new.double()
    Outputs.Perimeter = new.double()
    Outputs.Area = new.double()

def __exceptions__():
    pass

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
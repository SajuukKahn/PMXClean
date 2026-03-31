# DisplayName = Flush
# Description = Flush the solvent and purge cups for the set duration
# Icon = WaterPumpMaterialIcon
# SubIcon = CupWaterMaterialIcon
# Flags = IsTriggerStep, IsProcessStep

def __inputs__():
    #Description = The amount of time to flush
    Inputs.Duration = new.double(2, .1, 15, .1, 1, "s")

def __run__():
    output = Settings.FlushOutput
    if output is None:
        __throwexception__(Exceptions.OutputMissing)

    output.Set(True)
    PVA.System.Wait(Inputs.Duration.Value * 1000.0)
    output.Set(False)

def __virtual__():
    PVA.System.Wait(Inputs.Duration.Value * 1000.0)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    output = Settings.FlushOutput
    if output is not None:
        output.SetAsync(False)

def __exceptionrecovery__():
    pass
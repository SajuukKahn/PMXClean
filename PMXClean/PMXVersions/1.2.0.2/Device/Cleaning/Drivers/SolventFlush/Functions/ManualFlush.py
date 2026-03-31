#DisplayName = Manual Flush
#Description = Flush the solvent and purge cups using the time set in configuration.
#Icon = CupWaterMaterialIcon
#SubIcon = SyncMaterialIcon
#Flags = IsMappable, IsQuickAction

def __inputs__():
    pass

def __run__():
    output = Settings.FlushOutput
    if output is None:
        __throwexception__(Exceptions.OutputMissing)

    output.Set(True)
    PVA.System.Wait(Settings.ManualFlushTime.Value * 1000)
    output.Set(False)

def __virtual__():
    __run__()

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
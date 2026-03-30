#DisplayName = Set Translation
#Description = Sets the Translation output of the parent Inspection
#Icon = CursorMoveMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #Description = The translation offset, defined in mm
    Inputs.Translation = new.translation()

def __run__():
    if Inputs.Translation is None:
        __throwexception__(Exceptions.TranslationInputMissing)
        return

    SetTranslationOutputInternal(Inputs.Translation)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.TranslationInputMissing = new.exception("#Inspection.Exceptions.TranslationInputMissingTitle", "#Inspection.Exceptions.TranslationInputMissing", new.enum("Severity", "Error").Value, None)

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
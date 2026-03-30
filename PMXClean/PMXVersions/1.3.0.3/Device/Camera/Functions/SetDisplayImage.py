#DisplayName = Set Header Display
#Description = Sets the Header Display image
#Icon = MonitorScreenshotMaterialIcon
#Flags = IsHidden, IsInspectionStep, IsProgramStep

def __inputs__():
    #CanReference = Linked
    #Description = The image to display
    Inputs.Image = new.image(0, 0, False, True)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    SetAsDisplayImage(Inputs.Image)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    if PVA.Inspection.IsDesignTime():
        PVA.Inspection.WarnException(exception)
    else:
        PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
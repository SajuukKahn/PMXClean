#DisplayName = Save Image
#Description = Saves an image to the provided disk location
#Icon = ContentSaveMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #Description = The input image to save to disk
    Inputs.Image = new.image(0, 0, False, True)

    #Description = The directory to save images to
    Inputs.Directory = new.directory(None, "mim", True)

    #DisplayName = Run At Design Time
    #Description = Whether to run this step during design time, or only when running production
    Inputs.RunAtDesignTime = new.bool(False)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if not Inputs.RunAtDesignTime.Value and PVA.Inspection.IsDesignTime():
        return

    savePath = Inputs.Directory.GeNewFileName()

    if savePath is None:
        __throwexception__(Exceptions.SavePathFailed)
        return

    SaveImageInternal(Inputs.Image, savePath, False)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OperationFailed = new.exception("#Inspection.Exceptions.OperationFailedTitle", "#Inspection.Exceptions.OperationFailed", new.enum("Severity", "Error").Value, None)
    Exceptions.SavePathFailed = new.exception("#Inspection.Exceptions.SavePathFailedTitle", "#Inspection.Exceptions.SavePathFailed", new.enum("Severity", "Error").Value, None)

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
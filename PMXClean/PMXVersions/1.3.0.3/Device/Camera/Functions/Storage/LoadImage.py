#DisplayName = Load Image
#Description = Loads an image from the provided disk location
#Icon = UploadMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #DisplayName = File Path
    #Description = The path on disk to load the image from
    Inputs.FilePath = new.file(None, None, r"Image Files(*.mim)|*.mim", True)

def __run__():
    LoadImageInternal(Inputs.FilePath, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    Outputs.Image = new.image()

def __exceptions__():
    Exceptions.OperationFailed = new.exception("#Inspection.Exceptions.OperationFailedTitle", "#Inspection.Exceptions.OperationFailed", new.enum("Severity", "Error").Value, None)

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
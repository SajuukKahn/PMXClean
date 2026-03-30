#DisplayName = Remove Region
#Description = Removes the last applied region of interest from the specified image
#Icon = StickerMinusMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #Description = The image to remove the region of interest from
    Inputs.Image = new.image()

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    RemoveRegionOfInterestInternal(Inputs.Image, Outputs.AnnotatedImage, Outputs.Image)

def __virtual__():
    pass

def __outputs__():
    #Description = The image with without the selected Region of Interest
    Outputs.Image = new.image()

    #DisplayName = Annotated Image
    #Description = A preview image after the region of interest has been removed
    Outputs.AnnotatedImage = new.image(3, 0, False, False, True)

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)

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
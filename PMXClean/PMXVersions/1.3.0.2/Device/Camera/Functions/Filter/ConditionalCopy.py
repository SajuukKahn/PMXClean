#DisplayName = Conditional Copy
#Description = Conditionally copies the content of the Source Image atop a copy of the Destination Image, based on the provided mask
#Icon = CodeBracesMaterialIcon
#SubIcon = ContentCopyMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Source Image
    #Description = The input image to conditionally copy into the Destination Image
    Inputs.SourceImage = new.image()
    
    #Optional = True
    #Enabled = False
    #CanReference = Linked
    #Description = This image's non-zero pixels will copy corresponding pixels from the Source Image to the Output Image, if disabled, the whole image will copy. If both the Source Image and Mask are multi-band, the copy condition is evaluated per-band. This mask image can be any size, as it will be resized to match the Source image
    Inputs.Mask = new.image(0, 0, False, True)
    
    #Description = inverts the mask logic
    Inputs.Invert = new.bool()

    #Optional = True
    #CanReference = Linked
    #DisplayName = Destination Image
    #Description = The image that will be copied into the Output Image in its entirety before the conditional copy is applied, if disabled, a new image will be allocated matching the Source Image's size
    Inputs.DestinationImage = new.image()

def __run__():
    if Inputs.SourceImage is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.SourceImage.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    ConditionalCopyInternal(Inputs.SourceImage, Inputs.Mask, Inputs.DestinationImage, Inputs.Invert, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after conditionally copying pixels atop the Destination Image
    Outputs.Image = new.image()

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
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
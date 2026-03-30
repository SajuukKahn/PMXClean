#DisplayName = Conditional Clear
#Description = Conditionally clears the content of an image based on the provided mask
#Icon = CodeBracesMaterialIcon
#SubIcon = EraserVariantMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()
    RegisterCallback("Image", __on_source_image_changed__, True)

    #Optional = True
    #Enabled = False
    #CanReference = Linked
    #Description = This image's non-zero pixels will clear corresponding pixels from the Image. If both the Image and Mask are multi-band, this is evaluated on a per-band basis. This mask image can be any size, as it will be resized to match
    Inputs.Mask = new.image(0, 0, False, True)

    #Description = inverts the mask logic
    Inputs.Invert = new.bool()

    #Optional = True
    #Enabled = False
    #DisplayName = Clear Color
    #Description = The color to use when clearing pixels, if unchecked, clears to the minimum pixel value for the image
    Inputs.ClearColor = new.color(0, 0, 0)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    ConditionalClearInternal(Inputs.Image, Inputs.Mask, Inputs.Invert, Inputs.ClearColor, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after conditionally clearing pixels
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

def __on_source_image_changed__():
    sourceImage = Inputs.Image.GetCurrentValue()
    if sourceImage is not None:
        Inputs.ClearColor.Grayscale = sourceImage.GetBandCount() == 1
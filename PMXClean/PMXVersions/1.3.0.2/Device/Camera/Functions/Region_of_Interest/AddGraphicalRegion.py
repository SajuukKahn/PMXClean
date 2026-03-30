#DisplayName = Add Graphical Region
#Description = Graphically create a region within an image upon which future inspection steps will be limited to
#Icon = StickerPlusMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()

    #DisplayName = Region of Interest
    #Description = The region of interest to set on the input image
    Inputs.ROI = new.region()

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    SetRegionOfInterestInternal(Inputs.Image, Inputs.ROI, Outputs.AnnotatedImage, Outputs.Image)

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Image
    #Description = The image with applied region of interest
    Outputs.Image = new.image()

    #DisplayName = Annotated Image
    #Description = The image after the region of interest has been applied, for preview purposes
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
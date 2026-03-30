#DisplayName = Add Variable Region
#Description = Dynamically creates a rectangular Region of Interest from input values that limits the scope of future operations
#Icon = StickerCodeCustomIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Mono Image
    Inputs.Image = new.image(1)
    RegisterCallback("Image", __on_image_changed__, True)

    #CanReference = True
    #Description = The left value for the region of interest
    Inputs.Left = new.int(0, 0)
    RegisterCallback("Left", __on_left_changed__, True)

    #CanReference = True
    #Description = The top value for the region of interest
    Inputs.Top = new.int(0, 0)
    RegisterCallback("Top", __on_top_changed__, True)

    #Optional = True
    #CanReference = True
    #Description = The width value for the region of interest, if disabled, uses the remaining width of the image less the value of Left
    Inputs.Width = new.int(0, 0)

    #Optional = True
    #CanReference = True
    #Description = The height value for the region of interest, if disabled, uses the remaining height of the image less the value of Top
    Inputs.Height = new.int(0, 0)

    #CanReference = True
    #Description = Whether the region of interest is inclusive or exclusive
    Inputs.Invert = new.bool()

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    CreateRegionOfInterestInternal(Inputs.Image, Inputs.Left, Inputs.Top, Inputs.Width, Inputs.Height, Inputs.Invert, Outputs.AnnotatedImage, Outputs.Image)

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

def __on_image_changed__():
    image = Inputs.Image.GetCurrentValue()
    if image is not None and image.Identifier != 0:
        height = image.GetHeight()
        if height is not None:
            Inputs.Top.ConstantValue.MaximumValue = height - 1

        width = image.GetWidth()
        if width is not None:
            Inputs.Left.ConstantValue.MaximumValue = width - 1

def __on_top_changed__():
    image = Inputs.Image.GetCurrentValue()
    if image is not None and image.Identifier != 0:
        height = image.GetHeight()
        if height is not None:
            top = Inputs.Top.GetCurrentValue()
            if top is not None:
                Inputs.Height.ConstantValue.MaximumValue = height - top.Value

def __on_left_changed__():
    image = Inputs.Image.GetCurrentValue()
    if image is not None and image.Identifier != 0:
        width = image.GetWidth()
        if width is not None:
            left = Inputs.Left.GetCurrentValue()
            if left is not None:
                Inputs.Width.ConstantValue.MaximumValue = width - left.Value
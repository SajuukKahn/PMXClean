#DisplayName = Create Image
#Description = Creates an image using the provided settings
#Icon = ImagePlusMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = True
    #Description = Defines the width of the image to create
    Inputs.Width = new.int(1920, 2, None)
    Inputs.Width.IsCalculatedValue = True
    
    #CanReference = True
    #Description = Defines the height of the image to create
    Inputs.Height = new.int(1080, 2, None)
    Inputs.Height.IsCalculatedValue = True

    #CanReference = True
    #DisplayName = Allocate Color Image
    #Description = If True, allocates a color (3-band) image, otherwise allocates a mono (1-band) image
    Inputs.Color = new.bool(True)
    RegisterCallback("Color", __on_bands_changed__, True)

    #DisplayName = Fill Color
    #Description = The color used to fill the created image
    Inputs.FillColor = new.color(0, 0, 0)

def __run__():
    if Inputs.Width is None or Inputs.Height is None:
        __throwexception__(Exceptions.InputSizeNotSet)
        return

    if Inputs.Color is None:
        __throwexception__(Exceptions.InputAllocateColorMissing)
        return

    CreateImageInternal(Inputs.Width, Inputs.Height, Inputs.Color, Inputs.FillColor, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The newly created image
    Outputs.Image = new.image(3)

def __exceptions__():
    Exceptions.InputSizeNotSet = new.exception("#Inspection.Exceptions.InputSizeNotSetTitle", "#Inspection.Exceptions.InputSizeNotSet", new.enum("Severity", "Error").Value, None)
    Exceptions.InputAllocateColorMissing = new.exception("#Inspection.Exceptions.InputAllocateColorMissingTitle", "#Inspection.Exceptions.InputAllocateColorMissing", new.enum("Severity", "Error").Value, None)
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

def __on_bands_changed__():
    color = Inputs.Color.GetCurrentValue()
    if color is not None and not color.Value:
        Outputs.Image.ExpectedBands = 1
        Inputs.FillColor.Grayscale = True
    else:
        Outputs.Image.ExpectedBands = 3
        Inputs.FillColor.Grayscale = False
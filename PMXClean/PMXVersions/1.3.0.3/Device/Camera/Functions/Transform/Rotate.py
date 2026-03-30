#Description = Rotate an image around the image's center
#Icon = FormatRotate90MaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()
    RegisterCallback("Image", __on_image_changed__, True)

    #CanReference = True
    Inputs.Rotation = new.double(0, -360.00, 360.00, 0.01, 15, u"\u00b0")
    
    #CanReference = True
    #DisplayName = Rotate Clockwise
    #Description = Whether the rotation is in the clockwise direction. Useful for undoing a known rotation
    Inputs.RotateClockwise = new.bool(False);

    #Optional = True
    #Enabled = False
    #CanReference = True
    #Description = The left offset of the output image, if disabled, uses the image's center. When in use, cannot size output image to extent
    Inputs.Left = new.int(0, 0, None, 1, 20, "px")
    RegisterCallback("Left", __on_center_changed__, True)

    #Optional = True
    #Enabled = False
    #CanReference = True
    #Description = The top offset of the output image, if disabled, uses the image's center. When in use, cannot size output image to extent
    Inputs.Top = new.int(0, 0, None, 1, 20, "px")
    RegisterCallback("Top", __on_center_changed__, True)

    #CanReference = True
    #DisplayName = Size Output Image To Extent
    #Description = Whether to size the output image to the extent of the rotated image or lose some data by keeping the image size from the source
    Inputs.SizeToExtent = new.bool()

    #DisplayName = Fill Color
    #Description = The color used to fill any empty areas created by the rotation
    Inputs.FillColor = new.color()

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Rotation is None:
        __throwexception__(Exceptions.RotationInputMissing)
        return

    RotateInternal(Inputs.Image, Inputs.Rotation, Inputs.RotateClockwise, Inputs.Left, Inputs.Top, Inputs.SizeToExtent, Inputs.FillColor, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after rotating. Note that after performing the operation, the image will not be calibrated, even if the source image was calibrated
    Outputs.Image = new.image()

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.RotationInputMissing = new.exception("#Inspection.Exceptions.RotationInputMissingTitle", "#Inspection.Exceptions.RotationInputMissing", new.enum("Severity", "Error").Value, None)
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

def __on_image_changed__():
    image = Inputs.Image.GetCurrentValue()
    if image is not None and image.Identifier != 0:
        bandCount = image.GetBandCount()
        if bandCount is not None:
            Inputs.FillColor.Grayscale = bandCount == 1

        height = image.GetHeight()
        if height is not None:
            Inputs.Top.ConstantValue.MaximumValue = height - 1

        width = image.GetWidth()
        if width is not None:
            Inputs.Left.ConstantValue.MaximumValue = width - 1

def __on_center_changed__():
    top = Inputs.Top.GetCurrentValue()
    left = Inputs.Left.GetCurrentValue()
    if top is None and left is None:
        Inputs.SizeToExtent.IsPrivate = False;
    else:
        Inputs.SizeToExtent.IsPrivate = True;
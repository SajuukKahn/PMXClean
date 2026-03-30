#Description = Resize an image to the specified height and width, scaling the pixel data
#Icon = OverscanMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()
    
    #CanReference = True
    #Description = The desired width of the output image in pixels
    Inputs.Width = new.int(1024, 2, None, 1, 20, "px")
    Inputs.Width.IsCalculatedValue = True

    #CanReference = True
    #Description = The desired height of the output image in pixels
    Inputs.Height = new.int(1024, 2, None, 1, 20, "px")
    Inputs.Height.IsCalculatedValue = True

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    ResizeDiscreteInternal(Inputs.Image, Inputs.Width, Inputs.Height, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after resizing. Note that after performing the operation, the image will not be calibrated, even if the source image was calibrated
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
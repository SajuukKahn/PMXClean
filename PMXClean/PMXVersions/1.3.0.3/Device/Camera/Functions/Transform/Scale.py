#Description = Resize an image by the specified scaling factor(s)
#Icon = ResizeMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()

    #CanReference = True
    #Description = The scale factor to use for the image
    Inputs.Scale = new.double(1, 0.01, 8, 0.01, 0.1, "[Unit]", __unitproviders__.percent)

    #Optional = True
    #Enabled = False
    #CanReference = True
    #DisplayName = Vertical Scale
    #Description = If enabled, the scale to use independently for the vertical aspect
    Inputs.VerticalScale = new.double(1, 0.01, 8, 0.01, 0.1, "[Unit]", __unitproviders__.percent)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    ResizePercentileInternal(Inputs.Image, Inputs.Scale, Inputs.VerticalScale, Outputs.Image)

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
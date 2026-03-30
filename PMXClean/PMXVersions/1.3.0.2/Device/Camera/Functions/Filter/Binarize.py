#Description = Performs a binary threshold operation, setting pixels to either maximum or minimum values based on the thresholding settings
#Icon = ImageFilterBlackWhiteMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()
    RegisterCallback("Image", __on_image_changed__, True)
    
    #DisplayName = Threshold
    Inputs.FirstThreshold = new.range(0, 255, 0)
    
    #Private = True
    #DisplayName = Second Band Threshold
    Inputs.SecondThreshold = new.range(0, 255, 0)

    #Private = True
    #DisplayName = Third Band Threshold
    Inputs.ThirdThreshold = new.range(0, 255, 0)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    BinarizeInternal(Inputs.Image, Inputs.FirstThreshold, Inputs.SecondThreshold, Inputs.ThirdThreshold, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after binarization
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

def __on_image_changed__():
    image = Inputs.Image.GetCurrentValue()
    if image is not None and image.Identifier != 0:
        if image.GetBandCount() == 3:
            Inputs.FirstThreshold.DisplayName = "First Band Threshold"
            Inputs.SecondThreshold.IsPrivate = False
            Inputs.ThirdThreshold.IsPrivate = False
        else:
            Inputs.FirstThreshold.DisplayName = "Threshold"
            Inputs.SecondThreshold.IsPrivate = True
            Inputs.ThirdThreshold.IsPrivate = True

        maxPX = image.GetMaximumPixelValue()
        if maxPX is not None:
            Inputs.FirstThreshold.MaximumValue = maxPX
            Inputs.SecondThreshold.MaximumValue = maxPX
            Inputs.ThirdThreshold.MaximumValue = maxPX

        minPX = image.GetMinimumPixelValue()
        if minPX is not None:
            Inputs.FirstThreshold.MinimumValue = minPX
            Inputs.SecondThreshold.MinimumValue = minPX
            Inputs.ThirdThreshold.MinimumValue = minPX
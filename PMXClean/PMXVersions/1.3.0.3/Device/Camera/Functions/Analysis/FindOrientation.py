#DisplayName = Find Orientation
#Description = Finds the dominant orientation of the source image using the consistent spatial patterns in the image
#Icon = CompassMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Mono Image
    #Description = The input image to analyze, must be a one-band image
    Inputs.Image = new.image(1)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return
        
    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.GetBandCount() != 1:
        __throwexception__(Exceptions.ImageInputInvalid)
        return

    FindOrientationInternal(Inputs.Image, Outputs.Orientation)

def __virtual__():
    pass

def __outputs__():
    Outputs.Orientation = new.double(0, -360, 360, 0.01, 15, u"\u00b0")

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ImageInputInvalid = new.exception("#Inspection.Exceptions.InputImageInvalidTitle", "#Inspection.Exceptions.InputImageInvalid", new.enum("Severity", "Error").Value, None)
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
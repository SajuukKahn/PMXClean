#DisplayName = Reset Origin
#Description = Moves the Calibration Relative Origin back to the center of the image
#Icon = DotsGridMaterialIcon
#SubIcon = ArrowULeftTopMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Calibrated Image
    #Description = The Image with an associated Calibration to reset the Relative Origin on
    Inputs.CalibratedImage = new.image(0, 0, True)

def __run__():
    if Inputs.CalibratedImage is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.CalibratedImage.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.CalibratedImage.CalibrationIdentifier == 0:
        __throwexception__(Exceptions.ImageInputNotCalibrated)
        return
        
    ResetOriginInternal(Inputs.CalibratedImage)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ImageInputNotCalibrated = new.exception("#Inspection.Exceptions.ImageInputNotCalibratedTitle", "#Inspection.Exceptions.ImageInputNotCalibrated", new.enum("Severity", "Error").Value, None)
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
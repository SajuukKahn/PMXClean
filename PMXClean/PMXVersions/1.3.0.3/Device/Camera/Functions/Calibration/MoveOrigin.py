#DisplayName = Move Origin
#Description = Moves the Calibration Relative Origin relative to its current position
#Icon = DotsGridMaterialIcon
#SubIcon = CursorMoveMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Calibrated Image
    #Description = The Image with an associated Calibration to apply the relative origin move to
    Inputs.CalibratedImage = new.image(0, 0, True)
    
    #CanReference = True
    #DisplayName = X Offset
    #Description = The distance to move the origin along the X axis
    Inputs.XOffset = new.double(0.0, -55.0, 55.0, 0.1, 1.0, "mm")
    
    #CanReference = True
    #DisplayName = Y Offset
    #Description = The distance to move the origin along the Y axis
    Inputs.YOffset = new.double(0.0, -55.0, 55.0, 0.1, 1.0, "mm")

    #CanReference = True
    #Description = The rotation to apply to the origin in degrees. Positive values rotate the origin clockwise, negative values rotate it counter-clockwise
    Inputs.Rotation = new.double(0.0, -180.0, 180.0, 5.0, 45.0, "\u00B0")

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

    MoveOriginInternal(Inputs.CalibratedImage, Inputs.XOffset, Inputs.YOffset, Inputs.Rotation)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ImageInputNotCalibrated = new.exception("#Inspection.Exceptions.ImageInputNotCalibratedTitle", "#Inspection.Exceptions.ImageInputNotCalibrated", new.enum("Severity", "Error").Value, None)

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
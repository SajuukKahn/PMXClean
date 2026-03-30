#DisplayName = Draw Calibration
#Description = Draws Calibration data destructively on a new output image
#Icon = DotsGridMaterialIcon
#SubIcon = BrushMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Calibrated Image
    #Description = The Image with an associated Calibration to draw
    Inputs.CalibratedImage = new.image(0, 0, True, True)

    #DisplayName = Graphics Color
    #Description = The color to use when drawing the calibration graphics
    Inputs.GraphicsColor = new.color(0, 0, 225)

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

    DrawCalibrationInternal(Inputs.CalibratedImage, Inputs.GraphicsColor, Outputs.AnnotatedImage)

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Annotated Image
    #Description = A copy of the Calibrated Image with the Calibration data drawn destructively
    Outputs.AnnotatedImage = new.image(3, 0, False, False, True)

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Info").Value, None)
    Exceptions.ImageInputNotCalibrated = new.exception("#Inspection.Exceptions.ImageInputNotCalibratedTitle", "#Inspection.Exceptions.ImageInputNotCalibrated", new.enum("Severity", "Info").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetExecutingStepName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
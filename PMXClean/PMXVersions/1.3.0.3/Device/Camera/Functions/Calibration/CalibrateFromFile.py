#DisplayName = Calibrate from File
#Description = Transforms the image and associates the real world unit mm to the image and defines the center of the image as the origin 0,0 for location coordinates
#Icon = DotsGridMaterialIcon
#SubIcon = FileMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()

    #Description = The Calibration that is sourced from disk to apply to the input image
    Inputs.Calibration = new.calibration()

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.CalibrationIdentifier != 0:
        __throwexception__(Exceptions.AlreadyCalibrated)
        return

    if not Inputs.Calibration.IsValid():
        __throwexception__(Exceptions.CalibrationNotValid)
        return

    PVA.Inspection.CalibrateImage(Inputs.Image, Inputs.Calibration, Outputs.CalibratedImage)

    if Outputs.CalibratedImage.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Calibrated Image
    Outputs.CalibratedImage = new.image()

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.CalibrationNotValid = new.exception("#Inspection.Exceptions.CalibrationNotValidTitle", "#Inspection.Exceptions.CalibrationNotValid", new.enum("Severity", "Error").Value, None)
    Exceptions.AlreadyCalibrated = new.exception("#Inspection.Exceptions.AlreadyCalibratedTitle", "#Inspection.Exceptions.AlreadyCalibrated", new.enum("Severity", "Error").Value, None)
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
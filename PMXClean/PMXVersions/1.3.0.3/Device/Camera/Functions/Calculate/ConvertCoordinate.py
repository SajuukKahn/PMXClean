#DisplayName = Convert Coordinate
#Description = Converts a coordinate in a given space to another coordinate space using the calibration of the provided image
#Icon = VectorLineDottedCustomIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Calibrated Image
    #Description = The Image with an associated Calibration
    Inputs.CalibratedImage = new.image(0, 0, True)

    Inputs.Conversion = new.enum("ConversionDirection", "PixelToWorld")
    RegisterCallback("Conversion", __on_conversion_changed__, True)
    
    #Optional = True
    #CanReference = True
    #DisplayName = Left
    #Description = The horizontal coordinate to convert, if disabled, uses the center of the image for pixels, or zero for world coordinates
    Inputs.Horizontal = new.double()

    #Optional = True
    #CanReference = True
    #DisplayName = Top
    #Description = The vertical coordinate to convert, if disabled, uses the center of the image for pixels, or zero for world coordinates
    Inputs.Vertical = new.double()

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

    ConvertCoordinateInternal(Inputs.CalibratedImage, Inputs.Conversion.Value, Inputs.Horizontal, Inputs.Vertical, Outputs.Horizontal, Outputs.Vertical)

def __virtual__():
    pass

def __outputs__():
    #DisplayName = X
    Outputs.Horizontal = new.double()

    #DisplayName = Y
    Outputs.Vertical = new.double()

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

def __on_conversion_changed__():
    if Inputs.Conversion is not None and str(Inputs.Conversion.Value) == "WorldToPixel":
        Inputs.Horizontal.ConstantValue.DisplayName = "X"
        Inputs.Vertical.ConstantValue.DisplayName = "Y"
        Inputs.Horizontal.ConstantValue.Units = "mm"
        Inputs.Vertical.ConstantValue.Units = "mm"
        Inputs.Horizontal.ConstantValue.DecimalCount = 3
        Inputs.Vertical.ConstantValue.DecimalCount = 3

        Outputs.Horizontal.DisplayName = "Left"
        Outputs.Vertical.DisplayName = "Top"
        Outputs.Horizontal.DecimalCount = 0
        Outputs.Vertical.DecimalCount = 0
        Outputs.Horizontal.Units = "px"
        Outputs.Vertical.Units = "px"
    else:
        Inputs.Horizontal.ConstantValue.DisplayName = "Left"
        Inputs.Vertical.ConstantValue.DisplayName = "Top"
        Inputs.Horizontal.ConstantValue.Units = "px"
        Inputs.Vertical.ConstantValue.Units = "px"
        Inputs.Horizontal.ConstantValue.DecimalCount = 0
        Inputs.Vertical.ConstantValue.DecimalCount = 0

        Outputs.Horizontal.DisplayName = "X"
        Outputs.Vertical.DisplayName = "Y"
        Outputs.Horizontal.DecimalCount = 3
        Outputs.Vertical.DecimalCount = 3
        Outputs.Horizontal.Units = "mm"
        Outputs.Vertical.Units = "mm"
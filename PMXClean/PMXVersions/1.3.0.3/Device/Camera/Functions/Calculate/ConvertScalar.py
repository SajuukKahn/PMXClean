#DisplayName = Convert Scalar
#Description = Converts a scalar in a given space's units to another space's units using the calibration of the provided image
#Icon = DatabaseMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Calibrated Image
    #Description = The Image with an associated Calibration
    Inputs.CalibratedImage = new.image(0, 0, True)
    
    Inputs.Conversion = new.enum("ConversionDirection", "PixelToWorld")
    RegisterCallback("Conversion", __on_conversion_changed__, True)
    
    Inputs.Operation = new.enum("ConversionOperation", "Length")
    RegisterCallback("Operation", __on_operation_changed__, True)
    
    #CanReference = True
    #Description = The scalar value to convert
    Inputs.Scalar = new.double(1)

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

    ConvertScalarInternal(Inputs.CalibratedImage, Inputs.Conversion.Value, Inputs.Operation.Value, Inputs.Scalar, Outputs.ConvertedScalar)

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Converted Scalar
    Outputs.ConvertedScalar = new.double()

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

def __on_operation_changed__():
    __on_conversion_changed__()

def __on_conversion_changed__():
    unitTag = ""
    if Inputs.Operation is not None and str(Inputs.Operation.Value) == "Area":
        unitTag = u"\u00b2"
        
    if Inputs.Conversion is not None and str(Inputs.Conversion.Value) == "WorldToPixel":
        Inputs.Scalar.ConstantValue.Units = "mm" + unitTag
        Inputs.Scalar.ConstantValue.DecimalCount = 3
        Inputs.Scalar.ConstantValue.MinimumValue = 0.001
        Outputs.ConvertedScalar.DecimalCount = 0
        Outputs.ConvertedScalar.Units = "px" + unitTag
    else:
        Inputs.Scalar.ConstantValue.Units = "px" + unitTag
        Inputs.Scalar.ConstantValue.DecimalCount = 0
        Inputs.Scalar.ConstantValue.MinimumValue = 1
        Outputs.ConvertedScalar.DecimalCount = 3
        Outputs.ConvertedScalar.Units = "mm" + unitTag
#DisplayName = Convert Image
#Description = Converts an image according to the provided settings
#Icon = FormatPageSplitMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Color Image
    #Description = The input image to convert, must be a three-band image
    Inputs.Image = new.image(3)

    #Description = The conversion to perform. Some selections will change the output image to a single band
    Inputs.Conversion = new.enum("ConversionType", "RGBtoL")
    RegisterCallback("Conversion", __on_conversion_changed__, True)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return
        
    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.GetBandCount() != 3:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    ConvertImageInternal(Inputs.Image, Inputs.Conversion.Value, Outputs.Image)
    
    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after conversion. The number of bands varies by the selected conversion
    Outputs.Image = new.image(1)

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

def __on_conversion_changed__():
    if (len(str(Inputs.Conversion.Value)) < 7):
        Outputs.Image.ExpectedBands = 1
    else:
        Outputs.Image.ExpectedBands = 3
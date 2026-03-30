#DisplayName = Extract Band
#Description = Copies a specified band of the specified source image to a new image
#Icon = SetMergeMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Color Image
    Inputs.Image = new.image(3)

    #DisplayName = Source Band
    #Description = The source band to extract from the input image
    Inputs.SourceBand = new.int(0, 0, 2, 1, 1)

    #DisplayName = Output Color Image
    #Description = Whether the output image will be in color or a single band
    Inputs.OutputColorImage = new.bool()
    RegisterCallback("OutputColorImage", __on_output_color_image_changed__, True)

    #Optional = True
    #Enabled = False
    #Private = True
    #DisplayName = Output Target Band
    #Description = The band in the output image to place the source band into, if unchecked, uses the Source Band value
    Inputs.TargetBand = new.int(0, 0, 2, 1, 1)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return
        
    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.GetBandCount() != 3:
        __throwexception__(Exceptions.ImageInputInvalid)
        return

    ExtractBandInternal(Inputs.Image, Inputs.SourceBand, Inputs.OutputColorImage, Inputs.TargetBand, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after extracting the band
    Outputs.Image = new.image(1)

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

def __on_output_color_image_changed__():
    if Inputs.OutputColorImage.Value:
        Outputs.Image.ExpectedBands = 3
        Inputs.TargetBand.IsPrivate = False
    else:
        Outputs.Image.ExpectedBands = 1
        Inputs.TargetBand.IsPrivate = True
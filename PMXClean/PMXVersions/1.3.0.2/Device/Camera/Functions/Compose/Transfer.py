#Description = Copies an area of one or all bands of the Source Image to an area of one or all bands of the Destination Image
#Icon = MoveResizeVariantMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Source Image
    #Description = The source image to copy an area of pixels from
    Inputs.SourceImage = new.image()
    RegisterCallback("SourceImage", __on_source_image_changed__, True)

    #CanReference = True
    #DisplayName = Source Left
    #Description = The offset from the left of the Source Image to copy
    Inputs.SourceLeft = new.int(0, 0)
    RegisterCallback("SourceLeft", __on_source_left_changed__, True)

    #CanReference = True
    #DisplayName = Source Top
    #Description = The offset from the top of the Source Image to copy
    Inputs.SourceTop = new.int(0, 0)
    RegisterCallback("SourceTop", __on_source_top_changed__, True)

    #Optional = True
    #CanReference = True
    #DisplayName = Source Width
    #Description = If enabled and non-zero, defines the width of the source area to copy from, otherwise, uses the full width of the Source Image, less the Source Offset X Value
    Inputs.SourceWidth = new.int(0, 0)

    #Optional = True
    #CanReference = True
    #DisplayName = Source Height
    #Description = If enabled and non-zero, defines the height of the source area to copy from, otherwise, uses the full height of the Source Image, less the Source Offset Y Value
    Inputs.SourceHeight = new.int(0, 0)
    
    #CanReference = Linked
    #DisplayName = Destination Image
    #Description = An image that is copied into the Output Image before the source area is copied and defines the Output Image size
    Inputs.DestinationImage = new.image()
    RegisterCallback("DestinationImage", __on_destination_image_changed__, True)

    #CanReference = True
    #DisplayName = Destination Left
    #Description The position of the top left pixel within the output image that the Source Image's defined area will be placed at
    Inputs.DestinationLeft = new.int(0, 0)

    #CanReference = True
    #DisplayName = Destination Top
    #Description The position of the top left pixel within the output image that the Source Image's defined area will be placed at
    Inputs.DestinationTop = new.int(0, 0)

def __run__():
    if Inputs.SourceImage is None or Inputs.DestinationImage is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.SourceImage.Identifier == 0 or Inputs.DestinationImage.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    TransferInternal(Inputs.SourceImage, Inputs.DestinationImage, Inputs.SourceLeft, Inputs.SourceTop, Inputs.SourceWidth, Inputs.SourceHeight, Inputs.DestinationLeft, Inputs.DestinationTop, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after transferring the Source Image's defined area. Note that after performing the operation, the image will not be calibrated, even if the Source Image was calibrated
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

def __on_source_image_changed__():
    sourceImage = Inputs.SourceImage.GetCurrentValue()
    if sourceImage is not None and sourceImage.Identifier != 0:

        width = sourceImage.GetWidth()
        if width is not None:
            Inputs.SourceLeft.ConstantValue.MaximumValue = width - 1
            __on_source_top_changed__()
        
        height = sourceImage.GetHeight()
        if height is not None:
            Inputs.SourceTop.ConstantValue.MaximumValue = height - 1
            __on_source_left_changed__()

def __on_destination_image_changed__():
    destinationImage = Inputs.DestinationImage.GetCurrentValue()
    if destinationImage is not None and destinationImage.Identifier != 0:

        width = destinationImage.GetWidth()
        if width is not None:
            Inputs.DestinationLeft.ConstantValue.MaximumValue = width - 1

        height = destinationImage.GetHeight()
        if height is not None:
            Inputs.DestinationTop.ConstantValue.MaximumValue = height - 1

def __on_source_top_changed__():
    sourceImage = Inputs.SourceImage.GetCurrentValue()
    if sourceImage is not None and sourceImage.Identifier != 0:
        sourceTop = Inputs.SourceTop.GetCurrentValue()
        if sourceTop is not None:
            height = sourceImage.GetHeight()
            if height is not None:
                Inputs.SourceHeight.ConstantValue.MaximumValue = height - sourceTop.Value

def __on_source_left_changed__():
    sourceImage = Inputs.SourceImage.GetCurrentValue()
    if sourceImage is not None and sourceImage.Identifier != 0:
        sourceLeft = Inputs.SourceLeft.GetCurrentValue()
        if sourceLeft is not None:
            width = sourceImage.GetWidth()
            if width is not None:
                Inputs.SourceWidth.ConstantValue.MaximumValue = width - sourceLeft.Value
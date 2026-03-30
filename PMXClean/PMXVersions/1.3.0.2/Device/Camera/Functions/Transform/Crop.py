#Description = Crops an image according to the provided settings
#Icon = CropMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()
    RegisterCallback("Image", __on_image_changed__, True)
    
    #CanReference = True
    Inputs.Left = new.int(0, 0, None, 1, 20, "px")
    RegisterCallback("Left", __on_left_changed__, True)

    #CanReference = True
    Inputs.Top = new.int(0, 0, None, 1, 20, "px")
    RegisterCallback("Top", __on_top_changed__, True)

    #Optional = True
    #CanReference = True
    #Description = If non-zero, defines the width of the cropped area, otherwise uses the full width of the image less the Left offset
    Inputs.Width = new.int(0, 0, None, 1, 20, "px")
    
    #Optional = True
    #CanReference = True
    #Description = If non-zero, defines the height of the cropped area, otherwise uses the full height of the image less the Top offset
    Inputs.Height = new.int(0, 0, None, 1, 20, "px")

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return
        
    CropInternal(Inputs.Image, Inputs.Left, Inputs.Top, Inputs.Width, Inputs.Height, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after cropping
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

def __on_image_changed__():
    image = Inputs.Image.GetCurrentValue()
    if image is not None and image.Identifier != 0:
        height = image.GetHeight()
        if height is not None:
            Inputs.Top.ConstantValue.MaximumValue = height - 1
            __on_top_changed__()

        width = image.GetWidth()
        if width is not None:
            Inputs.Left.ConstantValue.MaximumValue = width - 1
            __on_left_changed__()

def __on_top_changed__():
    image = Inputs.Image.GetCurrentValue()
    if image is not None and image.Identifier != 0:
        top = Inputs.Top.GetCurrentValue()
        if top is not None:
            height = image.GetHeight()
            if height is not None:
                Inputs.Height.ConstantValue.MaximumValue = height - top.Value

def __on_left_changed__():
    image = Inputs.Image.GetCurrentValue()
    if image is not None and image.Identifier != 0:
        left = Inputs.Left.GetCurrentValue()
        if left is not None:
            width = image.GetWidth()
            if width is not None:
                Inputs.Width.ConstantValue.MaximumValue = width - left.Value
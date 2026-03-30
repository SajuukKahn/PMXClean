#Description = Performs a morphological operation on an image
#Icon = ShimmerMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()

    #Description = The Morhpological operation to perform
    Inputs.Operation = new.enum("Morphology", "Erode")
    RegisterCallback("Operation", __on_operation_changed__, True)

    #CanReference = True
    #DisplayName = Iterations
    #Description = The number of times to perform the operation sequentially
    Inputs.Scalar = new.int(1, 0, 65535, 1, 10)

    #DisplayName = Structuring Element
    #Description = Defines the weights of pixels around a central element that is aligned with each pixel of the image to determine how the pixel is modified
    Inputs.StructuringElement = new.structure()
    
    #Description = Whether to perform a binary operation where any non-zero pixel is considered as 1
    Inputs.Binary = new.bool()

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    MorphologyInternal(Inputs.Image, Inputs.Operation.Value, Inputs.Scalar, Inputs.StructuringElement, Inputs.Binary, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after the operation
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

def __on_operation_changed__():
    operation = str(Inputs.Operation.Value)
    if "Area" in operation:
        Inputs.Scalar.DisplayName = "Minimum Area"
        Inputs.Scalar.Description = "The minimum area in pixels"
        Inputs.Scalar.ConstantValue.MinimumValue = 4
        Inputs.Scalar.ConstantValue.MaximumValue = 6000000
        Inputs.Scalar.ConstantValue.Units = u"px\u00b2"
        Inputs.Scalar.ConstantValue.SmallStep = 4
        Inputs.Scalar.ConstantValue.LargeStep = 1000
    else:
        Inputs.Scalar.DisplayName = "Iterations"
        Inputs.Scalar.Description = "The number of times to perform the operation sequentially"
        Inputs.Scalar.ConstantValue.MinimumValue = 0
        Inputs.Scalar.ConstantValue.MaximumValue = 65535
        Inputs.Scalar.ConstantValue.Units = ""
        Inputs.Scalar.ConstantValue.SmallStep = 1
        Inputs.Scalar.ConstantValue.LargeStep = 10

    if "Hat" in operation or "hat" in operation or "Level" in operation or "level" in operation:
        Inputs.Binary.IsPrivate = True
    else:
        Inputs.Binary.IsPrivate = False
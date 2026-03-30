#DisplayName = Arithmetic
#Description = Performs arithmetic operations on an image
#Icon = FunctionMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()

    #Description = The mathematical operation to perform
    Inputs.Operation = new.enum("Arithmetic", "Addition")
    RegisterCallback("Operation", __on_operation_changed__, True)

    #Optional = True
    #Enabled = False
    #CanReference = Linked
    #DisplayName = Second Image
    #Description = A secondary image that the operation utilizes to calculate values of corresponding pixels
    Inputs.SecondImage = new.image()

    #Optional = False
    #CanReference = True
    #Description = The numeric value to use in the arithmetic operation
    Inputs.Constant = new.double(25, -255, 255, 0.1, 1)

    #Private = True
    #DisplayName = Swap Operands
    #Description = Swaps the operands in the operation (e.g., Constant - Image instead of Image - Constant)
    Inputs.SwapOperands = new.bool()

    #Private = True
    #DisplayName = Invert Operation
    #Description = Inverts the operation e.g. 'Equal' becomes 'Not Equal', 'AND becomes NAND', for unary 'Equals', negates the image's values
    Inputs.Invert = new.bool()

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    ArithmeticInternal(Inputs.Image, Inputs.Operation.Value, Inputs.SecondImage, Inputs.Constant, Inputs.SwapOperands, Inputs.Invert, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after arithmetic operations
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
    bools = ArithmeticOperationFlags(Inputs.Operation.Value)
    # [0] hide swap
    # [1] hide invert
    # [2] hide image
    # [3] image optional
    # [4] hide constant
    # [5] constant optional

    Inputs.SwapOperands.IsPrivate = bools[0]
    Inputs.Invert.IsPrivate = bools[1]
    Inputs.SecondImage.IsPrivate = bools[2]
    Inputs.SecondImage.IsOptional = bools[3]
    Inputs.Constant.IsPrivate = bools[4]
    Inputs.Constant.IsOptional = bools[5]

    if Inputs.SecondImage.IsPrivate:
        Inputs.SecondImage.IsEnabled = False

    if not Inputs.SecondImage.IsOptional:
        Inputs.SecondImage.IsEnabled = True
        
    if Inputs.Constant.IsPrivate:
        Inputs.Constant.IsEnabled = False
        
    if not Inputs.Constant.IsOptional:
        Inputs.Constant.IsEnabled = True
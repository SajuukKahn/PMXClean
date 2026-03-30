#DisplayName = Draw Graphics
#Description = Draws the specified graphic items destructively onto the image
#Icon = ShapeMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image(0, 0, False, True)

    Inputs.Graphics = new.graphics("defaultCheckmarkGraphic")

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    DrawGraphicsInternal(Inputs.Image, Inputs.Graphics, Outputs.AnnotatedImage)

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Annotated Image
    #Description = The resulting image after graphics are drawn
    Outputs.AnnotatedImage = new.image(3, 0, False, False, True)

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Info").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetExecutingStepName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
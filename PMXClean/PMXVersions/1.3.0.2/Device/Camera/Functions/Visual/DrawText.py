#DisplayName = Draw Text
#Description = Draws the specified text destructively onto the image at the specified location
#Icon = FormatTextboxMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image(0, 0, False, True)
    RegisterCallback("Image", __on_image_changed__, True)

    #CanReference = True
    Inputs.Text = new.string("DATA")

    #CanReference = True
    #Optional = True
    #Enabled = False
    #Description = the distance from the left of the image to draw the text, if disabled, uses the center of the image
    Inputs.Left= new.int(250, 0, None, 1, 20, "px")

    #CanReference = True
    #Optional = True
    #Enabled = False
    #Description = the distance from the top of the image to draw the text, if disabled, uses the center of the image
    Inputs.Top = new.int(250, 0, None, 1, 20, "px")
    
    #DisplayName = Foreground
    #Description = The color to use for the text
    Inputs.Foreground = new.color(0, 255, 0)

    #Optional = True
    #DisplayName = Background
    #Description = The color to use for the the text background, if disabled, the text is drawn without a background
    Inputs.Background = new.color(0, 0, 0)

    #DisplayName = Font Settings
    #Description = The font settings that define the appearance of the drawn text as well as its alignment
    Inputs.FontSettings = new.font()

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    DrawTextInternal(Inputs.Image, Inputs.Text, Inputs.Left, Inputs.Top, Inputs.Foreground, Inputs.Background, Inputs.FontSettings, Outputs.AnnotatedImage)

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Annotated Image
    #Description = The resulting image after text is placed
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

def __on_image_changed__():
    image = Inputs.Image.GetCurrentValue()
    if image is not None:
        if image.Identifier != 0:
            height = image.GetHeight()
            if height is not None:
                Inputs.Top.ConstantValue.MaximumValue = height - 1
            width = image.GetWidth()
            if width is not None:
                Inputs.Left.ConstantValue.MaximumValue = width - 1
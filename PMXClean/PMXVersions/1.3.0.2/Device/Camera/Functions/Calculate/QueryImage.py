#DisplayName = Query Image
#Description = Queries an image and outputs all of its data
#Icon = ImageTextMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image(0, 0, False, True)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    bands = Inputs.Image.GetBandCount()
    bits = Inputs.Image.GetBitDepth()
    width = Inputs.Image.GetWidth()
    height = Inputs.Image.GetHeight()
    maxValue = Inputs.Image.GetMaximumPixelValue()
    minValue = Inputs.Image.GetMinimumPixelValue()

    Outputs.BandCount.Value = bands if bands is not None else 0
    Outputs.Width.Value = width if width is not None else 0
    Outputs.Height.Value = height if height is not None else 0
    Outputs.MinPixelValue.Value = minValue if minValue is not None else 0.0
    Outputs.MaxPixelValue.Value = maxValue if maxValue is not None else 0.0
    Outputs.IsAnnotated.Value = Inputs.Image.IsAnnotated
    Outputs.EdgeDataDestroyed.Value = Inputs.Image.AreEdgesDestroyed
    Outputs.RegionCount.Value = len(Inputs.Image.Regions)
    Outputs.CalibrationID.Value = Inputs.Image.CalibrationIdentifier

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Band Count
    #Description = The number of bands in the image
    Outputs.BandCount = new.int()

    #Description = The width of the image in pixels
    Outputs.Width = new.int()

    #Description = The height of the image in pixels
    Outputs.Height = new.int()

    #DisplayName = Minimum Pixel Value
    #Description = The minimum possible value of any pixel in the image
    Outputs.MinPixelValue = new.double()

    #DisplayName = Maximum Pixel Value
    #Description = The maximum possible value of any pixel in the image
    Outputs.MaxPixelValue = new.double()

    #DisplayName = Is Annotated
    #Description = Whether the image has annotations and cannot be used for analysis
    #Private = True
    Outputs.IsAnnotated = new.bool(False, True)

    #DisplayName = Edge Data Destroyed
    #Description = Whether the edge data of the image has been destroyed
    #Private = True
    Outputs.EdgeDataDestroyed = new.bool(False, True)

    #DisplayName = Region Count
    #Description = The number of Regions of Interest applied to this image
    Outputs.RegionCount = new.int()

    #DisplayName = Calibration ID
    #Description = The calibration ID of the image
    Outputs.CalibrationID = new.int()

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
    Outputs.BandCount.IsPrivate = True
    Outputs.Width.IsPrivate = True
    Outputs.Height.IsPrivate = True
    Outputs.MinPixelValue.IsPrivate = True
    Outputs.MaxPixelValue.IsPrivate = True
    Outputs.IsAnnotated.IsPrivate = True
    Outputs.EdgeDataDestroyed.IsPrivate = True
    Outputs.RegionCount.IsPrivate = True
    Outputs.CalibrationID.IsPrivate = True

def __exceptionrecovery__():
    pass
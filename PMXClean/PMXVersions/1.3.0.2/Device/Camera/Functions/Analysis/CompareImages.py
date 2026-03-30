#DisplayName = Compare Images
#Description = Compares the two images, and rating their similarity. The images must be 1-band images of the same width and height. Results are most consitent with binarized images as Gain and other noise can cause a lowering of Similarity
#Icon = ImageSearchMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    Inputs.Image = new.image()
    
    #CanReference = Linked
    #DisplayName = Reference Image
    Inputs.ReferenceImage = new.image()

def __run__():
    if Inputs.Image is None or Inputs.ReferenceImage is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return
        
    if Inputs.Image.Identifier == 0 or Inputs.ReferenceImage.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.GetBandCount() != Inputs.ReferenceImage.GetBandCount():
        __throwexception__(Exceptions.ImageInputMismatchedBands)
        return

    if Inputs.Image.GetWidth() != Inputs.ReferenceImage.GetWidth() or Inputs.Image.GetHeight() != Inputs.ReferenceImage.GetHeight():
        __throwexception__(Exceptions.ImageInputsMismatchedSize)
        return

    CompareImagesInternal(Inputs.Image, Inputs.ReferenceImage, Outputs.Similarity)

def __virtual__():
    pass

def __outputs__():
    #Description = The percentile similarity of the two images
    Outputs.Similarity = new.double(1, 0.01, 1, 0.0001, 0.1, "[Unit]", __unitproviders__.percent)

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ImageInputMismatchedBands = new.exception("#Inspection.Exceptions.ImageInputMismatchedBandsTitle", "#Inspection.Exceptions.ImageInputMismatchedBands", new.enum("Severity", "Error").Value, None)
    Exceptions.ImageInputsMismatchedSize = new.exception("#Inspection.Exceptions.ImageInputsMismatchedSizeTitle", "#Inspection.Exceptions.ImageInputsMismatchedSize", new.enum("Severity", "Error").Value, None)
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
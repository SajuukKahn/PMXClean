#DisplayName = Assign Bands
#Description = Copies each source image's specified band to the Output Image's bands
#Icon = LayersTripleMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Band One Image
    #Description = The input image to extract a band from and insert into the first band of the output image
    Inputs.BandOneImage = new.image()
    RegisterCallback("BandOneImage", __on_band_one_image_changed__, True)
    
    #DisplayName = Band One Source Band
    #Description = The source band to extract from the Band One Image
    Inputs.BandOneSourceBand = new.int(0, 0, 2)
    
    #CanReference = Linked
    #DisplayName = Band Two Image
    #Description = The input image to extract a band from and insert into the second band of the output image
    Inputs.BandTwoImage = new.image()
    RegisterCallback("BandTwoImage", __on_band_two_image_changed__, True)
    
    #DisplayName = Band Two Source Band
    #Description = The source band to extract from the Band Two Image
    Inputs.BandTwoSourceBand = new.int(1, 0, 2)

    #CanReference = Linked
    #DisplayName = Band Three Image
    #Description = The input image to extract a band from and insert into the third band of the output image
    Inputs.BandThreeImage = new.image()
    RegisterCallback("BandThreeImage", __on_band_three_image_changed__, True)
    
    #DisplayName = Band Three Source Band
    #Description = The source band to extract from the Band Three Image
    Inputs.BandThreeSourceBand = new.int(2, 0, 2)

def __run__():
    if Inputs.BandOneImage is None or Inputs.BandTwoImage is None or Inputs.BandThreeImage is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return
        
    if Inputs.BandOneImage.Identifier == 0 or Inputs.BandTwoImage.Identifier == 0 or Inputs.BandThreeImage.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return
        
    if Inputs.BandOneImage.GetWidth() != Inputs.BandTwoImage.GetWidth() or Inputs.BandTwoImage.GetWidth() != Inputs.BandThreeImage.GetWidth() or Inputs.BandOneImage.GetWidth() != Inputs.BandThreeImage.GetWidth():
        __throwexception__(Exceptions.ImageInputsMismatchedSize)
        return
        
    if Inputs.BandOneImage.GetHeight() != Inputs.BandTwoImage.GetHeight() or Inputs.BandTwoImage.GetHeight() != Inputs.BandThreeImage.GetHeight() or Inputs.BandOneImage.GetHeight() != Inputs.BandThreeImage.GetHeight():
        __throwexception__(Exceptions.ImageInputsMismatchedSize)
        return

    AssignBandsInternal(Inputs.BandOneImage, Inputs.BandOneSourceBand, Inputs.BandTwoImage, Inputs.BandTwoSourceBand, Inputs.BandThreeImage, Inputs.BandThreeSourceBand, Outputs.Image)

    if Outputs.Image.Identifier == 0:
        __throwexception__(Exceptions.OperationFailed)

def __virtual__():
    pass

def __outputs__():
    #Description = The resulting image after blending bands
    Outputs.Image = new.image(3)

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
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

def __on_band_one_image_changed__():
    bandOneImage = Inputs.BandOneImage.GetCurrentValue()
    if bandOneImage is None or bandOneImage.GetBandCount() != 3:
        Inputs.BandOneSourceBand.IsPrivate = True
    else:
        Inputs.BandOneSourceBand.IsPrivate = False

def __on_band_two_image_changed__():
    bandTwoImage = Inputs.BandTwoImage.GetCurrentValue()
    if bandTwoImage is None or bandTwoImage.GetBandCount() != 3:
        Inputs.BandTwoSourceBand.IsPrivate = True
    else:
        Inputs.BandTwoSourceBand.IsPrivate = False

def __on_band_three_image_changed__():
    bandThreeImage = Inputs.BandThreeImage.GetCurrentValue()
    if bandThreeImage is None or bandThreeImage.GetBandCount() != 3:
        Inputs.BandThreeSourceBand.IsPrivate = True
    else:
        Inputs.BandThreeSourceBand.IsPrivate = False
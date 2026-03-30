#DisplayName = Pattern Search
#Description = Finds the selected pattern of pixels in the input image and outputs the position data. For Calibrated input images, the output is in millimeters relative to the Calibration Reference Origin, for uncalibrated images, the output is in pixels relative to the top-left of the image
#Icon = CardSearchMaterialIcon
#Flags = IsHidden, IsInspectionStep

def __inputs__():
    #CanReference = Linked
    #DisplayName = Mono Image
    #Description = The input image to analyze, must be a one-band image
    Inputs.Image = new.image(1)
    
    #Description = The pattern data to search for in the input image
    Inputs.Pattern = new.pattern()

    #DisplayName = Target Match Score
    #Description = The minimum matching score a matching pattern must achieve to be considered a valid match
    Inputs.TargetMatchScore = new.int(70, 5, 100, 1, 5, "%")

    #Optional = True
    #Enabled = False
    #DisplayName = Angular Range
    #Description = Specifies the angular bounds to search for the pattern, the search will start at zero degrees if it lies within the range, otherwise, it will start at the median angle
    Inputs.AngularRange = new.range(-180, 180, 1, u"\u00b0", False)

    #DisplayName = Match Priority
    #Description = Specifies the preference of selecting the best match when multiple matches are found
    Inputs.MatchPreference = new.enum("MatchPreference", "ClosestToOrigin")

    #DisplayName = Show All Matches
    #Description = Whether to display all found matches in the output image, or only the best match according to the Match Priority
    Inputs.ShowAllMatches = new.bool(False)

def __run__():
    if Inputs.Image is None:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.Identifier == 0:
        __throwexception__(Exceptions.ImageInputMissing)
        return

    if Inputs.Image.GetBandCount() != 1:
        __throwexception__(Exceptions.ImageInputInvalid)
        return

    if Inputs.Pattern.Definition is None:
        __throwexception__(Exceptions.PatternMissing)
        return

    if not ImageHasCompatibleRegions(Inputs.Image, "Pattern"):
        __throwexception__(Exceptions.IncompatibleROI)
        return

    PatternSearchInternal(Inputs.Image, Inputs.Pattern, Inputs.TargetMatchScore, Inputs.AngularRange, Inputs.MatchPreference.Value, Inputs.ShowAllMatches, Outputs.MatchScore, Outputs.Left, Outputs.Top, Outputs.Rotation, Outputs.NumberOfPassingMatches, Outputs.Translation, Outputs.AnnotatedImage)

    if Inputs.AngularRange is not None:
        Outputs.RotationEnabled.Value = Inputs.AngularRange.IsEnabled and Inputs.AngularRange.LowValue != 0 and Inputs.AngularRange.HighValue != 0
    else:
        Outputs.RotationEnabled.Value = False

    Outputs.Passed.Value = (Outputs.MatchScore.Value * 100) >= Inputs.TargetMatchScore.Value

def __virtual__():
    pass

def __outputs__():
    #Description = Indicates whether the target Acceptance Score was met
    Outputs.Passed = new.bool(False, True)

    #DisplayName = Match Score
    #Description = The score of the found match
    Outputs.MatchScore = new.double(1, 0.00, 1, 0.0001, 0.1, "[Unit]", __unitproviders__.percent)

    #Description = The pixel location of the matched pattern's Reference Position in the X direction
    Outputs.Left = new.double()

    #Description = The pixel location of the matched pattern's Reference Position in the Y direction
    Outputs.Top = new.double()

    #Description = The transform representing the translation of the matched pattern's Reference Position relative to the origin in a calibrated image
    Outputs.Translation = new.translation()

    #DisplayName = Rotational Search Enabled
    #Description = Denotes whether rotational searching was enabled for this result
    Outputs.RotationEnabled = new.bool(False, True)

    Outputs.Rotation = new.double(0, None, None, None, None, u"\u00b0")

    #DisplayName = Number of Passing Matches
    #Description = The number of passing matches found in the image, this does not consider the Match Preference setting or the Show All Matches setting
    Outputs.NumberOfPassingMatches = new.int()

    #DisplayName = Annotated Image
    #Description = The result image after matching that contains the match information requested
    Outputs.AnnotatedImage = new.image(3, 0, False, False, True)

def __exceptions__():
    Exceptions.ImageInputMissing = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ImageInputInvalid = new.exception("#Inspection.Exceptions.InputImageInvalidTitle", "#Inspection.Exceptions.InputImageInvalid", new.enum("Severity", "Error").Value, None)
    Exceptions.PatternMissing = new.exception("#Inspection.Exceptions.PatternMissingTitle", "#Inspection.Exceptions.PatternMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.IncompatibleROI = new.exception("#Inspection.Exceptions.PatternIncompatibleROITitle", "#Inspection.Exceptions.PatternIncompatibleROI", new.enum("Severity", "Error").Value, None)

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
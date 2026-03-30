#Description = Grabs an image with the provided settings
#Icon = CameraMaterialIcon
#Flags = IsHidden

def __inputs__():
    #DisplayName = Black Level
    Inputs.BlackLevel = new.acquisition(__source__, "BlackLevel")

    Inputs.Gain = new.acquisition(__source__, "Gain")

    #DisplayName = Exposure Time
    Inputs.ExposureTime = new.acquisition(__source__, "ExposureTime")

def __run__():
    if not PVA.Inspection.IsRunningLive() or (PVA.Inspection.IsDesignTime() and not GetConnectionState()):
        PVA.Inspection.LoadTestImage(Outputs.Image)

        if Outputs.Image.Identifier == 0:
            __throwexception__(Exceptions.TestImageLoadFailed)
            return

        return

    if not GetConnectionState():
        __throwexception__(Exceptions.NotConnected)
        return

    wasGrabbing = StopGrab()

    blackLevel = GetAcquisitionFeatureValue(Inputs.BlackLevel)
    gain = GetAcquisitionFeatureValue(Inputs.Gain)
    exposureTime = GetAcquisitionFeatureValue(Inputs.ExposureTime)

    SetAcquisitionFeatureValue(Inputs.BlackLevel, Inputs.BlackLevel.CurrentValue)
    SetAcquisitionFeatureValue(Inputs.Gain, Inputs.Gain.CurrentValue)
    SetAcquisitionFeatureValue(Inputs.ExposureTime, Inputs.ExposureTime.CurrentValue)

    GrabFrame(Outputs.Image)

    SetAcquisitionFeatureValue(Inputs.BlackLevel, blackLevel)
    SetAcquisitionFeatureValue(Inputs.Gain, gain)
    SetAcquisitionFeatureValue(Inputs.ExposureTime, exposureTime)

    if wasGrabbing:
        StartGrab()

def __virtual__():
    pass

def __outputs__():
    Outputs.Image = new.image()

def __exceptions__():
    Exceptions.NotConnected = new.exception("#Inspection.Exceptions.NotConnectedTitle", "#Inspection.Exceptions.NotConnected", new.enum("Severity", "Error").Value, None)
    Exceptions.TestImageLoadFailed = new.exception("#Inspection.Exceptions.TestImageLoadFailedTitle", "#Inspection.Exceptions.TestImageLoadFailed", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    if PVA.Inspection.IsDesignTime():
        PVA.Inspection.WarnException(exception)
    else:
        PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
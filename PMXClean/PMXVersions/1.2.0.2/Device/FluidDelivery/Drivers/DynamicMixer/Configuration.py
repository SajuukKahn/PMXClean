def __settings__():
    #DisplayName = Mixer Axis
    #Description = The axis driving this dynamic mixer
    Settings.MixerAxis = new.axis("Controller0", 0)

    #Description = The conversion rate to set the dispense rate in RPM
    Settings.Conversion = new.double(66.6667, 1, 999999999, 1, 10, "")

    #Optional = True
    #DisplayName = Mixer in Place Sensor
    #Description = The sensor that checks if the static mixer is present
    Settings.MixerInPlaceSensor = new.device("Proximity", 0)

def ready():
    if Settings.MixerAxis is None:
        __throwexception__(Exceptions.MixerAxisMissing)
        return

    if ((Settings.MixerInPlaceSensor is not None) and not Settings.MixerInPlaceSensor._PollState_.PolledState.Value):
        __throwexception__(Exceptions.MixerNotInPlace)
        return

    if (Settings.MixerAxis.Speed > Settings.MixerAxis.SpeedLimit):
        __throwexception__(Exceptions.PumpSpeedHigh)
        return

def __exceptions__():
    Exceptions.MixerAxisMissing = new.exception("#FluidDelivery.Exceptions.AxisMissingTitle", "#FluidDelivery.Exceptions.AxisMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.MixerNotInPlace = new.exception("#FluidDelivery.Exceptions.FluidDeliveryExceptionTitle", "#FluidDelivery.Exceptions.MixerNotInPlace", new.enum("Severity", "Error").Value, None)
    Exceptions.PumpSpeedHigh = new.exception("#FluidDelivery.Exceptions.FluidDeliveryExceptionTitle", "#FluidDelivery.Exceptions.DispenseRateHigh", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException
    (exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
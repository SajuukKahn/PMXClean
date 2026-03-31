#DisplayName = On
#Description = Turn the Dynamic Mixer on
#Icon = PowerPlugMaterialIcon

def __inputs__():
    pass

def __run__():
    axis = Settings.MixerAxis
    if axis is None:
        __throwexception__(Exceptions.AxisMissing)
        return

    controller = axis.GetController()
    if controller is None:
        __throwexception__(Exceptions.NoControllerConfigured)
        return

    if ((Settings.MixerInPlaceSensor is not None) and not Settings.MixerInPlaceSensor._PollState_.PolledState.Value):
        __throwexception__(Exceptions.MixerNotInPlace)
        return

    SetParameters(GetRate())

    axis.IsHomed.Value = True

    Ready()

    if axis.StopIssued.Value:
        prime(controller, axis)
        defineAxisPosition(controller, axis)

    controller.JogAxis(axis, axis.Speed.Value)

def __virtual__():
    pass

def prime(controller, axis):
    zeroJogPacket = new.string("JG" + axis.GetReferenceName() + "=0")
    controller.ExecuteCommand(zeroJogPacket)
    defineAxisPosition(controller, axis)
    servoAxis(controller, axis)
    controller.StopAxis(axis, False)

def defineAxisPosition(controller, axis):
    dpPacket = new.string("DP" + axis.GetReferenceName() + "=0")
    controller.ExecuteCommand(dpPacket)

def servoAxis(controller, axis):
    if (axis.Status.Count > 0 and axis.Status[0]):
        servoPacket = new.string("SH" + axis.GetReferenceName())
        controller.ExecuteCommand(servoPacket)
        PVA.System.Wait(250)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AxisMissing = new.exception("#FluidDelivery.Exceptions.AxisMissingTitle", "#FluidDelivery.Exceptions.AxisMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.NoControllerConfigured = new.exception("#Controller.Exceptions.MissingDeviceTitle", "#Controller.Exceptions.MissingDevice", new.enum("Severity", "Error").Value, None)
    Exceptions.MixerNotInPlace = new.exception("#FluidDelivery.Exceptions.FluidDeliveryExceptionTitle", "#FluidDelivery.Exceptions.MixerNotInPlace", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    axis = Settings.MixerAxis
    if axis is not None:
        controller = axis.GetController()
        if controller is not None:
            controller.StopAxis(axis, True)
            controller.ExecuteCommand(new.string("MO" + axis.GetReferenceName()))

def __exceptionrecovery__():
    pass
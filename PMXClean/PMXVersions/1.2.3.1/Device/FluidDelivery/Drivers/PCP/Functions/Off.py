#DisplayName = Off
#Description = Turn the PCP off
#Icon = PowerPlugOffMaterialIcon

def __inputs__():
    pass

def __run__():
    axis = Settings.PumpAAxis
    if axis is None:
        __throwexception__(Exceptions.AxisMissing)
        return

    controller = axis.GetController()
    if controller is None:
        __throwexception__(Exceptions.NoControllerConfigured)
        return

    suckbackDuration = GetSuckbackDuration()

    if suckbackDuration.Value > 0:
        axis.IsHomed.Value = True

        suckbackPacket = new.string("JG" + axis.GetReferenceName() + "=(-1*_JG" + axis.GetReferenceName() + ")")
        controller.ExecuteCommand(suckbackPacket)

        PVA.System.Wait(suckbackDuration.Value * 1000)

    controller.StopAxis(axis, False)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AxisMissing = new.exception("#FluidDelivery.Exceptions.AxisMissingTitle", "#FluidDelivery.Exceptions.AxisMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.NoControllerConfigured = new.exception("#Controller.Exceptions.MissingDeviceTitle", "#Controller.Exceptions.MissingDevice", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    axis = Settings.PumpAAxis
    if axis is not None:
        controller = axis.GetController()
        if controller is not None:
            controller.StopAxis(axis, True)

def __exceptionrecovery__():
    pass
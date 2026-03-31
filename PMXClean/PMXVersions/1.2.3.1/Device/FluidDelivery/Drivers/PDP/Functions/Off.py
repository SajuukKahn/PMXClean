#DisplayName = Off
#Description = Turn the PDP off
#Icon = PowerPlugOffMaterialIcon

def __inputs__():
    pass

def __run__():
    axisA = Settings.PumpAAxis
    if axisA is None:
        __throwexception__(Exceptions.AxisMissing)
        return

    axisB = Settings.PumpBAxis
    if axisB is None:
        __throwexception__(Exceptions.AxisMissing)
        return

    controller = axisA.GetController()
    if controller is None:
        __throwexception__(Exceptions.NoControllerConfigured)
        return

    referenceNameA = axisA.GetReferenceName()
    referenceNameB = axisB.GetReferenceName()

    suckbackDuration = GetSuckbackDuration()
    if suckbackDuration.Value > 0:
        axisA.IsHomed.Value = True
        axisB.IsHomed.Value = True
    
        suckbackPacket = new.string("JG" + referenceNameA + "=(-1*_JG" + referenceNameA + ");JG" + referenceNameB + "=(-1*_JG" + referenceNameB + ")")
        controller.ExecuteCommand(suckbackPacket)
    
        suckbackDuration = GetSuckbackDuration()
        PVA.System.Wait(suckbackDuration.Value * 1000)

    stopPacket = new.string("ST" + referenceNameA + referenceNameB)
    controller.ExecuteCommand(stopPacket)

    controller.StopAxis(axisA, False)
    controller.StopAxis(axisB, False)

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
    axisA = Settings.PumpAAxis
    axisB = Settings.PumpBAxis
    if (axisA is not None) and (axisB is not None):
        controller = axisA.GetController()
        if controller is not None:
            controller.StopAxis(axisA, True)
            controller.StopAxis(axisB, True)

def __exceptionrecovery__():
    pass
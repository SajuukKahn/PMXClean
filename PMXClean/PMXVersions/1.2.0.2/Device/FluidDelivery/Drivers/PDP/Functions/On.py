#DisplayName = On
#Description = Turn the PDP on and uses the last parameters set by the Set Parameters function.
#Icon = PowerPlugMaterialIcon

def __inputs__():
    pass

def __run__():
    axisA = GetPumpAAxis()
    if axisA is None:
        __throwexception__(Exceptions.AxisMissing)
        return

    axisB = GetPumpBAxis()
    if axisB is None:
        __throwexception__(Exceptions.AxisMissing)
        return

    controller = axisA.GetController()
    if controller is None:
        __throwexception__(Exceptions.NoControllerConfigured)
        return

    SetParameters(GetRate(), GetRatio(), GetSuckbackDuration(), Settings.NominalDisplacementA, Settings.NominalDisplacementB)

    axisA.IsHomed = True
    axisB.IsHomed = True

    Ready()

    if axisA.StopIssued.Value and axisB.StopIssued.Value:
        primeAxes(controller, axisA, axisB)
        defineAxesPosition(controller, axisA, axisB)
    elif axisA.StopIssued.Value:
        primeAxis(controller, axisA)
        defineAxisPosition(controller, axisA)
    elif axisB.StopIssued.Value:
        primeAxis(controller, axisB)
        defineAxisPosition(controller, axisB)

    controller.JogAxis(axisA, axisA.Speed.Value)
    controller.JogAxis(axisB, axisB.Speed.Value)

def __virtual__():
    pass

def primeAxes(controller, axisA, axisB):
    zeroJogPacket = new.string("JG" + axisA.ReferenceName + "=0;JG" + axisB.ReferenceName + "=0")
    controller.ExecuteCommand(zeroJogPacket)
    defineAxesPosition(controller, axisA, axisB)
    servoAxes(controller, axisA, axisB)
    controller.StopAxis(axisA, False)
    controller.StopAxis(axisB, False)

def defineAxesPosition(controller, axisA, axisB):
    dpPacket = new.string("DP" + axisA.ReferenceName + "=0;DP" + axisB.ReferenceName + "=0")
    controller.ExecuteCommand(dpPacket)

def servoAxes(controller, axisA, axisB):
    if (axisA.Status.Length > 0 and axisA.Status[0]):
        servoPacketA = new.string("SH" + axisA.ReferenceName)
        controller.ExecuteCommand(servoPacketA)

    if (axisB.Status.Length > 0 and axisB.Status[0]):
        servoPacketB = new.string("SH" + axisB.ReferenceName)
        controller.ExecuteCommand(servoPacketB)

    PVA.System.Wait(250)

def primeAxis(controller, axis):
    zeroJogPacket = new.string("JG" + axis.ReferenceName + "=0")
    controller.ExecuteCommand(zeroJogPacket)
    defineAxisPosition(controller, axis)
    servoAxis(controller, axis)
    controller.StopAxis(axis, False)

def defineAxisPosition(controller, axis):
    dpPacket = new.string("DP" + axis.ReferenceName + "=0")
    controller.ExecuteCommand(dpPacket)

def servoAxis(controller, axis):
    if (axis.Status.Length > 0 and axis.Status[0]):
        servoPacket = new.string("SH" + axis.ReferenceName)
        controller.ExecuteCommand(servoPacket)
        PVA.System.Wait(250)

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
    axisA = GetPumpAAxis()
    axisB = GetPumpBAxis()
    if (axisA is not None) and (axisB is not None):
        controller = axisA.GetController()
        if controller is not None:
            controller.StopAxis(axisA, True)
            controller.StopAxis(axisB, True)

def __exceptionrecovery__():
    pass
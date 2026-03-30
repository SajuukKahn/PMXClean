#DisplayName = Home Servo Adjust
#Description = Home the servo adjust axis
#Icon = HomeSwitchOutlineMaterialIcon
#Flags = IsTriggerStep

def __inputs__():
    #DisplayName = Wait for Signal
    #Description = A value indicating whether this script should wait for a signal before homing
    Inputs.WaitForHomingSignal = new.bool(False)

    #CanReference = True
    #Description = A value indicating whether to execute the PreAdjust function
    Inputs.PreAdjust = new.bool(False)

    #CanReference = True
    #Description = A value indicating whether to execute the PostAdjust function
    Inputs.PostAdjust = new.bool(False)

def __run__():
    findEdgeSpeed = new.int(1000)
    axis = GetAdjustmentAxis()
    if axis == None:
        __throwexception__(Exceptions.AxisMissing, "Adjustment")
        return

    controller = axis.GetController()
    if controller is None:
        __throwexception__(Exceptions.NoControllerConfigured)
        return

    if Inputs.WaitForHomingSignal and not axis.IsMotionReady:
        while not controller.GetHomingSignal():
            PVA.System.Wait(20)

    controller.HomeAxis(axis, findEdgeSpeed, not Inputs.WaitForHomingSignal)

def __virtual__():
    pass

def __outputs__():
    pass

def __lockresources__():
    axis = GetAdjustmentAxis()
    if axis is not None:
        controller = axis.GetController()
        if controller is not None:
            controller.RegisterAxisAsHoming(axis)
    if Inputs.PreAdjust.Value:
        PreAdjust()

def __releaseresources__():
    if Inputs.PostAdjust.Value:
        PostAdjust()
    axis = GetAdjustmentAxis()
    if axis is not None:
        controller = axis.GetController()
        if controller is not None:
            controller.DeregisterAxisAsHoming(axis)

def __exceptions__():
    Exceptions.AxisMissing = new.exception("#Controller.Exceptions.AxisNotSetTitle", "#Controller.Exceptions.AxisNotSet", new.enum("Severity", "Error").Value, None)
    Exceptions.NoControllerConfigured = new.exception("#Controller.Exceptions.MissingDeviceTitle", "#Controller.Exceptions.MissingDevice", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
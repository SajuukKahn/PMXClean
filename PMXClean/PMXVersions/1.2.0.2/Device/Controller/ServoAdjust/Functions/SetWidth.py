#DisplayName = Set Width
#Description = Set the servo adjust to a specified width
#Icon = ArrowLeftRightMaterialIcon
#Flags = IsProgramStep, IsTriggerStep

def __inputs__():
    #Description = The width to set the servo adjust to
    Inputs.Width = new.int(25000, -100000000, 100000000, 1000, 10000, "[Unit]", __source__)

    #Description = A value indicating whether to execute the PreAdjust trigger
    Inputs.PreAdjust = new.bool(False)

    #Description = A value indicating whether to execute the PostAdjust trigger
    Inputs.PostAdjust = new.bool(False)

def __run__():
    adjustmentAxisParameter = GetAdjustmentAxisParameter()
    if adjustmentAxisParameter == None:
        __throwexception__(Exceptions.AxisMissing, "Adjustment")
        return

    try:
        controller = getattr(PVA.Controllers, adjustmentAxisParameter.DeviceName)
    except:
        __throwexception__(Exceptions.NoControllerConfigured)
        return

    position = new.position(Inputs.Width.Value, adjustmentAxisParameter)

    controller.StopAxis(adjustmentAxisParameter, False)
    controller.ServoAxis(adjustmentAxisParameter)
    controller.MoveAxisToPosition(adjustmentAxisParameter, position)

def __virtual__():
    pass

def __outputs__():
    pass

def __lockresources__():
    if Inputs.PreAdjust.Value:
        PreAdjust()

def __releaseresources__():
    if Inputs.PostAdjust.Value:
        PostAdjust()

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
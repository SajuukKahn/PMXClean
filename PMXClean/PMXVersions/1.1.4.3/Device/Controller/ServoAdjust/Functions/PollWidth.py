# DisplayName = Poll Width
# Description = Poll the current width of the servo adjust
# Icon = PollMaterialIcon
# Flags = IsPolling, IsHidden

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    axis = GetAdjustmentAxisParameter()
    if axis is None:
        Outputs.PolledWidth.Value = 0.0
        if thrown:
            return
        thrown = True
        __throwexception__(Exceptions.AxisMissing, "Adjustment")
        return
    thrown = False
    GetCurrentWidth()
    Outputs.PolledWidth.Value = axis.Position

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Polled Width
    #Description = The current width of the servo adjust
    Outputs.PolledWidth = new.position(0, __source__)

def __exceptions__():
    Exceptions.AxisMissing = new.exception("#Controller.Exceptions.AxisNotSetTitle", "#Controller.Exceptions.AxisNotSet", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
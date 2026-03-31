# DisplayName = Motion Smoothing
# Description = Smooth the motion of moves for playback of abrupt direction changes
# Icon = IronMaterialIcon
# Flags = IsProgramStep, IsHidden
# Groups = Motion

# Sets the minimum percentage value, so 1% smoothing will correspond to approximately this value.
scaledMin = 0.5

# Value for maximum motion smoothing.
maxSmoothingValue = 0.004

def __inputs__():
    #DisplayName = Smoothing Percentage
    #Description = The percentage of smoothing to use
    Inputs.SmoothingPercentage = new.int(0, 0, 100, 1, 10, "")

    #Description = A value indicating the smoothing should apply to the X Axis
    Inputs.X = new.bool(False)

    #Description = A value indicating the smoothing should apply to the Y Axis
    Inputs.Y = new.bool(False)

    #Description = A value indicating the smoothing should apply to the Z Axis
    Inputs.Z = new.bool(False)

    #Optional = True
    #Description = A value indicating the smoothing should apply to the Theta Axis
    Inputs.W = new.bool(False)

def __run__():
    ActiveAxes = [["X", Inputs.X], ["Y", Inputs.Y], ["Z", Inputs.Z], ["W", Inputs.W]]
    smoothingValue = 1
    if Inputs.SmoothingPercentage.Value > 0:
        smoothingValue = scaledMin + ((maxSmoothingValue - scaledMin) / 100) * Inputs.SmoothingPercentage.Value
    try:
        commandToSend = ""
        for axis in ActiveAxes:
            if axis[1] is not None and axis[1].Value:
                commandToSend += "IT" + str(axis[0]) + '=' + str(round(smoothingValue, 4)) + ';'
        sendcommand(commandToSend)
    except:
        return

def __virtual__():
    pass

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

def __outputs__():
    pass

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
# DisplayName = Monitor Errors
# Description = Monitor the Galil for command and motor errors
# Icon = MonitorEyeMaterialIcon
# Flags = IsPolling, IsHidden

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    response = parseresponse(SendAndReceive("TC1", False))
    if response is None:
        __throwexception__(Exceptions.NoResponse, None)
        return
    if response != "0":
        Exceptions.CommandError.ExceptionData.MessageParams = tuple([GetDisplayName(), response])
        __throwexception__(Exceptions.CommandError, None)
        return
    for ax in GetAxes():
        if ax.IsActive:
            if ax.StopCode.Value == 2:
                Exceptions.MotorError.ExceptionData.MessageParams = tuple([GetDisplayName(), ax.DisplayName + " Forward Limit Error"])
                __throwexception__(Exceptions.MotorError, ax)
                return
            elif ax.StopCode.Value == 3:
                Exceptions.MotorError.ExceptionData.MessageParams = tuple([GetDisplayName(), ax.DisplayName + " Reverse Limit Error"])
                __throwexception__(Exceptions.MotorError, ax)
                return
            elif ax.StopCode.Value == 8:
                if ((abs(ax.PositionError.Value) > ax.ErrorLimit.Value) and (ax.ErrorLimit.Value > 0)):
                    Exceptions.MotorError.ExceptionData.MessageParams = tuple([GetDisplayName(), ax.DisplayName + " Position Error"])
                    __throwexception__(Exceptions.MotorError, ax)
                    return
                if (abs(ax.Torque.Value) > ax.TorqueLimit.Value):
                    Exceptions.MotorError.ExceptionData.MessageParams = tuple([GetDisplayName(), ax.DisplayName + " Torque Error"])
                    __throwexception__(Exceptions.MotorError, ax)
                    return
    if GetErrorOnBufferUnderrun():
        response = parseresponse(SendAndReceive("MG seq_err", False))
        if response == "1.0000":
            PrintLastMotionSequence()
            SendAndReceive("seq_err = 0", False)
            __throwexception__(Exceptions.BufferError, None)
            return
    clearexceptions()

def __virtual__():
    pass

def __outputs__():
    pass

def parseresponse(response):
    return response.rstrip(' :\t\r\n\0').lstrip(' ')

def clearexceptions():
    global thrown
    thrown = False
    for exception in list(Exceptions):
        exception.Value.Thrown.Value = False

def __exceptions__():
    Exceptions.CommandError = new.exception("#Controller.Exceptions.CommandErrorTitle", "#Controller.Exceptions.CommandError", new.enum("Severity", "Error").Value, None)
    Exceptions.MotorError = new.exception("#Controller.Exceptions.MotorErrorTitle", "#Controller.Exceptions.MotorError", new.enum("Severity", "Error").Value, None)
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.BufferError = new.exception("#Controller.Exceptions.BufferErrorTitle", "#Controller.Exceptions.BufferError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, axis):
    global thrown
    if not thrown:
        thrown = True
        if not exception.Thrown.Value:
            if (axis is not None):
                axis.IsHomed = False
            __exceptionhandling__()
            PVA.Exceptions.ThrowExceptionAsync(exception)

def __exceptionhandling__():
    ServoAxes()
    MotorOff()

def __exceptionrecovery__():
    pass
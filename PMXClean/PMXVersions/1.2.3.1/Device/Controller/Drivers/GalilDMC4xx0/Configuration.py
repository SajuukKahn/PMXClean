def __settings__():
    pass

def onconnect():
    # Galil specific settings with no class property
    sf = [1, 1, 1, 1, 1, 1, 1, 1]
    response = SendAndReceive("", False)
    if response is None or (not ":" in response and not "?" in response):
        throw

    response = sendcommand("QZ")

    qzvals = [parseresponse(value) for value in response.split(',')]
    axes = BuildAxes(qzvals[0])

    sendcommand("HX")
    sendcommand("ST")
    WaitMotionComplete(GetAxes())
    sendcommand("SH;MO") # SH to clear any current position error
    WaitMotorOff(GetAxes())
    sendcommand("TC1") # TC1 to clear current error
    sendcommand("CN,-1")

    # sending individually to avoid commands larger than 80 characters
    for axis in axes:
        referenceName = axis.GetReferenceName()
        sendcommand("FL" + referenceName + "=" + str(int(axis.ForwardLimit.Value)))
        sendcommand("BL" + referenceName + "=" + str(int(axis.ReverseLimit.Value)))
        sendcommand("TL" + referenceName + "=" + str(round(axis.TorqueLimit.Value, 4)))
        sendcommand("ER" + referenceName + "=" + (str(int(axis.ErrorLimit.Value)) if axis.IsActive else "-1"))
        sendcommand("OE" + referenceName + "=" + ("1" if axis.IsActive else "0"))
        sendcommand("SP" + referenceName + "=" + str(int(axis.Speed.Value)))
        sendcommand("AC" + referenceName + "=" + str(int(axis.Acceleration.Value)))
        sendcommand("DC" + referenceName + "=" + str(int(axis.Deceleration.Value)))
        sendcommand("KD" + referenceName + "=" + str(round(axis.DerivativeGain.Value, 4)))
        sendcommand("KP" + referenceName + "=" + str(round(axis.ProportionalGain.Value, 4)))
        sendcommand("KI" + referenceName + "=" + str(round(axis.IntegralGain.Value, 4)))

        sendcommand("SF" + referenceName + "=" + str(sf[axis.GetIndex()]))
        sendcommand("MT" + referenceName + "=" + str(convertMotorType(int(axis.GetMotorType()))))
        sendcommand("CE" + referenceName + "=" + str(int(axis.GetMainEncoderType())))
        sendcommand("BW" + referenceName + "=" + str(int(axis.BrakeWaitDelay.Value)))

    SetSpiralArcsThreshold(1) # number of spiral half-arcs from the center that will have their speed auto-adjusted
    SetErrorOnBufferUnderrun(True) # Set the flag indicating if the controller should thrown an error if a buffer underrun is detected.


def ondisconnect():
    sendcommand("ST")
    WaitMotionComplete(GetAxes())
    sendcommand("MO")
    sendcommand("HX")

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)

    if "?" in response:
        __throwexception__(Exceptions.CommandError, GetGalilError())

    if not ":" in response:
        __throwexception__(Exceptions.NotGalil, "GalilDMC4xx0")

    return response

def convertMotorType(motorType):
    if abs(motorType) > 10:
        return float(motorType / 10)
    return motorType

def parseresponse(command):
    if command is not None:
        return command.rstrip(' :\t\r\n\0')
    return command

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.NotGalil = new.exception("#Connection.Exceptions.InvalidDeviceTitle", "#Connection.Exceptions.InvalidDevice", new.enum("Severity", "Error").Value, None)
    Exceptions.CommandError = new.exception("#Controller.Exceptions.CommandErrorTitle", "#Controller.Exceptions.CommandError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
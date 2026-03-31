#DisplayName = Get Data Record
#Description = Get the data record from the Galil
#Icon = FormatListGroupMaterialIcon
#Flags = IsPolling, IsHidden

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown

    if Outputs.QZValues.Value is "":
        Outputs.QZValues.Value = sendcommand("QZ", 0, False)

    qzvals = [parseresponse(value) for value in Outputs.QZValues.Value.split(',')]
    byteCount = (int(qzvals[0]) * int(qzvals[3])) + int(qzvals[1]) + int(qzvals[2]) + 4
    Outputs.DataRecord.Value = SendAndReceiveBytes("QR", byteCount, True)

def __virtual__():
    pass

def sendcommand(command, byteCount, getBytes):
    global thrown
    if byteCount > 0:
        response = SendAndReceiveBytes(command, byteCount, getBytes)
    else:
        response = SendAndReceive(command, False)

    if response is None:
        if not thrown:
            __throwexception__(Exceptions.NoResponse)
            thrown = True
        raise

    if not getBytes and not ":" in response:
        if not thrown:
            __throwexception__(Exceptions.NotGalil, "GalilDMC4xx0")
            thrown = True
        raise

    return response

def parseresponse(command):
    if command is not None:
        return command.rstrip(' :\t\r\n\0')
    return command

def __outputs__():
    #Property = True
    #Private = True
    #DisplayName = Data Record
    #Description = The Data Record from the Galil
    Outputs.DataRecord = new.list()

    #Property = True
    #Private = True
    #DisplayName = QZ Values
    #Description = The values describing the number of axes on the Galil and size of the data record
    Outputs.QZValues = new.string()

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.NotGalil = new.exception("#Connection.Exceptions.InvalidDeviceTitle", "#Connection.Exceptions.InvalidDevice", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = Set IO Table
#Description = Build up the local IO table from the data record
#Icon = TableMaterialIcon
#Flags = IsPolling, IsHidden

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    axisBlockSize = 36
    encoders = []
    startingEncoderAddress = 98

    try:
        qzvals = [parseresponse(value) for value in _GetDataRecord_.QZValues.Value.split(',')]

        if qzvals is not None and qzvals[0] is not "":
            axisCount = int(qzvals[0])
            byteCount = (int(qzvals[0]) * int(qzvals[3])) + int(qzvals[1]) + int(qzvals[2]) + 4
            dataRecord = _GetDataRecord_.DataRecord.Value

            if dataRecord is None:
                return

            if axisCount < 0 or axisCount > 8:
                if not thrown:
                    __throwexception__(Exceptions.AxisCountError)
                raise

            for i in range(axisCount):
                encoders += [convertbytestosignedint(dataRecord, startingEncoderAddress + (axisBlockSize * i))]

            BuildInputTable(convertbytestobools(dataRecord, 6, 6), axisCount)
            BuildOutputTable(convertbytestobools(dataRecord, 16, 6), axisCount)
            BuildAnalogInputTable(getanaloginputs())
            BuildAnalogOutputTable(getanalogoutputs(), axisCount)
            BuildEncoders(encoders, axisCount)
            thrown = False
    except:
        thrown = True
        raise

def __virtual__():
    pass

def parseresponse(command):
    if command is not None:
        return command.rstrip(' :\t\r\n\0')
    return command

def sendcommand(message):
    global thrown
    response = SendAndReceive(message, False)

    if response is None:
        if not thrown:
            __throwexception__(Exceptions.NoResponse)
        raise

    return response

def convertbytestobools(dataRecord, startingaddress, size):
    bytestoconvert = dataRecord[startingaddress : startingaddress+size]
    bits_string = ''.join(format(int(byte), "b").zfill(8)[::-1] for byte in bytestoconvert)
    bools = [x == '1' for x in bits_string]
    return bools

def convertbytestosignedint(dataRecord, startingaddress):
    if (dataRecord[startingaddress + 3] & 0x80 == 0):
        intvalue = ((dataRecord[startingaddress + 3]) << 24) | ((dataRecord[startingaddress + 2]) << 16) | ((dataRecord[startingaddress + 1]) << 8) | (dataRecord[startingaddress])
    else:
        intvalue = ((((dataRecord[startingaddress + 3] ^ 0xFF) << 24) | ((dataRecord[startingaddress + 2] ^ 0xFF) << 16) | ((dataRecord[startingaddress + 1] ^ 0xFF) << 8) | (dataRecord[startingaddress] ^ 0xFF)) + 1) * -1
    return intvalue

def getanaloginputs():
    analogs = ["@AN[" + str(i+1) + "]" for i in range(8)]
    message = "MG " + ",".join(analogs)
    response = sendcommand(message)
    if response is None:
        return None
    floatvalues = [float(i) for i in response[response.find(" "):response.find("\r")].split()]
    return floatvalues

def getanalogoutputs():
    axes="ABCDEFGH"
    analogs = ["_OF" + str(i) for i in axes]
    message = "MG " + ",".join(analogs)
    response = sendcommand(message)
    if response is None:
        return None
    floatvalues = [float(i) for i in response[response.find(" "):response.find("\r")].split()]
    return floatvalues

def __outputs__():
    pass

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisCountError = new.exception("#Controller.Exceptions.AxisCountErrorTitle", "#Controller.Exceptions.AxisCountError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
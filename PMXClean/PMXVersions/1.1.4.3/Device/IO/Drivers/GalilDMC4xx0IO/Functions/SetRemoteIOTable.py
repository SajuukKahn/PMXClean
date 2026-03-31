# DisplayName = Set Remote IO Table
# Description = Build up the custom remote IO table
# Icon = TableClockMaterialIcon
# Flags = IsPolling, IsHidden

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown

    try:
        inputAddresses = GetRemoteInputAddresses()
        outputAddresses = GetRemoteOutputAddresses()

        inputValues = list()
        outputValues = list()

        for address in inputAddresses:
            result = sendcommand("MG@IN[" + str(address) + "]")
            if result == "1":
                inputValues.append(True)
            if result == "0":
                inputValues.append(False)

        for address in outputAddresses:
            result = sendcommand("MG@OUT[" + str(address) + "]")
            if result == "1":
                outputValues.append(True)
            if result == "0":
                outputValues.append(False)

        BuildRemoteInputTable(inputValues)
        BuildRemoteOutputTable(outputValues)

        thrown = False
    except:
        thrown = True
        return

def __virtual__():
    pass

def parseresponse(command):
    return command.split('.')[0].lstrip().rstrip(' :\t\r\n\0')

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

    return parseresponse(response)

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
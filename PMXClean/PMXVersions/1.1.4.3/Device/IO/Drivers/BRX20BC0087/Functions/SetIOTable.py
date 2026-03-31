# DisplayName = Set IO Table
# Description = Build up the local IO table from modbus commands
# Icon = TableMaterialIcon
# Flags = IsPolling, IsHidden

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    try:
        BuildInputTable(getdiscreteinputs())
        BuildOutputTable(getdiscreteoutputs())
        BuildAnalogOutputTable(getanalogoutputs())
        BuildAnalogInputTable(getanaloginputs())
        thrown = False
    except:
        thrown = True
        return

def __virtual__():
    pass

def sendCommand(command):
    response = SendAndReceive(command, False)
    if response is None:
        if thrown:
            return
        __throwexception__(Exceptions.NoResponse)
        return

    return response

def getdiscreteinputs():
    return tobits(sendCommand(BuildModbusPacket(2, 0, getdiscreteinputcount())))

def getdiscreteoutputs():
    return tobits(sendCommand(BuildModbusPacket(1, 0, getdiscreteoutputcount())))

def getanaloginputs():
    return towords(sendCommand(BuildModbusPacket(4, 0, getanaloginputcount())))

def getanalogoutputs():
    return towords(sendCommand(BuildModbusPacket(3, 0, getanalogoutputcount())))

def tobits(string):
    return [char for char in string]

def towords(string):
    return [convertwordtosignedint(string[i: i + 16]) for i in range(0, len(string), 16)]

def convertwordtosignedint(word):
    if (word[0] & 128 == 0):
        intvalue = (word[0] << 8) | word[1]
    else:
        intvalue = ((((word[0] ^ 0xFF) << 8) | (word[1] ^ 0xFF)) + 1) * -1
    return intvalue

def getdiscreteinputcount():
    inputRegisterCount = sendCommand(BuildModbusPacket(3, 4357, 1))
    inputRegisterSize = sendCommand(BuildModbusPacket(3, 4358, 1))
    return inputRegisterCount[0] * inputRegisterSize[0] * 8

def getdiscreteoutputcount():
    outputRegisterCount = sendCommand(BuildModbusPacket(3, 4359, 1))
    outputRegisterSize = sendCommand(BuildModbusPacket(3, 4360, 1))
    return outputRegisterCount[0] * outputRegisterSize[0] * 8

def getanaloginputcount():
    inputRegisterCount = sendCommand(BuildModbusPacket(3, 4353, 1))
    inputRegisterSize = sendCommand(BuildModbusPacket(3, 4354, 1))
    return inputRegisterCount[0] * inputRegisterSize[0] * 8

def getanalogoutputcount():
    outputRegisterCount = sendCommand(BuildModbusPacket(3, 4355, 1))
    outputRegisterSize = sendCommand(BuildModbusPacket(3, 4356, 1))
    return outputRegisterCount[0] * outputRegisterSize[0] * 8

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
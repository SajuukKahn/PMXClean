# DisplayName = Build Axis Data
# Description = Build up the local axis data tables from the Data Record
# Icon = TableMaterialIcon
# Flags = IsPolling, IsHidden

thrown = False

def __inputs__():
    pass

def __run__():
    global thrown
    axisBlockSize = 36
    motorStatus = []
    startingStatusAddress = 82
    homeSwitch = []
    startingHomeSwitchAddress = 84
    stopCode = []
    startingStopCodeAddress = 85
    position = []
    startingPositionAddress = 90
    positionError = []
    startingPositionErrorAddress = 94
    torque = []
    startingTorqueAddress = 106
    threadStatusAddress = 51
    threadStatus = []
    sAxisStartingStatusAddress = 64
    sAxisInMotion = False
    segmentAddress = 62

    try:
        qzvals = [parseresponse(value) for value in _GetDataRecord_.QZValues.Value.split(',')]
        if qzvals is not None and qzvals[0] is not "":
            axes = BuildAxes(int(qzvals[0]))
            axisCount = int(qzvals[0])
            dataRecord = _GetDataRecord_.DataRecord.Value

            if dataRecord is None:
                return

            for i in range(int(axisCount)):
                motorStatus.append(convertwordtobools(dataRecord, startingStatusAddress + (axisBlockSize * i)))
                position.append(convertbytestosignedint(dataRecord, startingPositionAddress + (axisBlockSize * i)))
                positionError.append(convertbytestosignedint(dataRecord, startingPositionErrorAddress + (axisBlockSize * i)))
                torque.append(convertbytestosignedint(dataRecord, startingTorqueAddress + (axisBlockSize * i)))
                homeSwitch.append(gethomeswitch(dataRecord, startingHomeSwitchAddress + (axisBlockSize * i)))
                stopCode.append(getstopcode(dataRecord, startingStopCodeAddress + (axisBlockSize * i)))

            threadStatus = convertbytetobools(dataRecord, threadStatusAddress)
            sAxisInMotion = getinmotion(dataRecord, sAxisStartingStatusAddress)
            segment = convertwordtounsignedint(dataRecord, segmentAddress)

            if axisCount > 8 or axisCount < 0:
                if not thrown:
                    __throwexception__(Exceptions.AxisCountError)
                    thrown = True
                return

            UpdateAxesData(motorStatus, position, positionError, torque, homeSwitch, threadStatus, stopCode, sAxisInMotion)
            UpdateGalilData(segment)
            thrown = False
    except:
        thrown = True
        raise

def __virtual__():
    pass

def convertwordtobools(dataRecord, startingaddress):
    bools=[]
    wordtoconvert = (dataRecord[startingaddress + 1] << 8) | dataRecord[startingaddress]
    bits_string = format(wordtoconvert, '16b')[::-1]
    bools = [x == '1' for x in bits_string]
    return bools

def convertbytetobools(dataRecord, startingaddress):
    bits_string = format(int(dataRecord[startingaddress]), '8b')[::-1]
    bools = [x == '1' for x in bits_string]
    return bools

def convertbytestosignedint(dataRecord, startingaddress):
    if (dataRecord[startingaddress + 3] & 0x80 == 0):
        intvalue = ((dataRecord[startingaddress + 3]) << 24) | ((dataRecord[startingaddress + 2]) << 16) | ((dataRecord[startingaddress + 1]) << 8) | (dataRecord[startingaddress])
    else:
        intvalue = ((((dataRecord[startingaddress + 3] ^ 0xFF) << 24) | ((dataRecord[startingaddress + 2] ^ 0xFF) << 16) | ((dataRecord[startingaddress + 1] ^ 0xFF) << 8) | (dataRecord[startingaddress] ^ 0xFF)) + 1) * -1
    return intvalue

def gettorque(dataRecord, startingaddress):
    floatvalue = float(convertbytestosignedint(dataRecord, startingaddress)) / 3276.8
    return floatvalue

def gethomeswitch(dataRecord, startingaddress):
    return dataRecord[startingaddress] & 2 == 0

def getstopcode(dataRecord, startingaddress):
    return int(dataRecord[startingaddress])

def getinmotion(dataRecord, startingaddress):
    return convertwordtobools(dataRecord, startingaddress)[15]

def convertwordtounsignedint(dataRecord, startingaddress):
    intvalue = (dataRecord[startingaddress + 1] << 8) | (dataRecord[startingaddress])
    return intvalue

def convertwordtosignedint(dataRecord, startingaddress):
    if (dataRecord[startingaddress + 1] & 128 == 0):
        intvalue = (dataRecord[startingaddress + 1] << 8) | (dataRecord[startingaddress])
    else:
        intvalue = ((((dataRecord[startingaddress + 1] ^ 0xFF) << 8) | (dataRecord[startingaddress] ^ 0xFF)) + 1) * -1
    return intvalue

def parseresponse(command):
    return command.rstrip(' :\t\r\n\0')

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AxisCountError = new.exception("#Controller.Exceptions.AxisCountErrorTitle", "#Controller.Exceptions.AxisCountError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
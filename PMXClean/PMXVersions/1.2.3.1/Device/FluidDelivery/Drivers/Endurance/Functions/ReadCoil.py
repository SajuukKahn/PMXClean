#DisplayName = Read Coil
#Description = Reads a single coil from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    #Description = The address of the coil to read
    Inputs.Address = new.int(21000)

def __run__():
    result = SendAndReceiveModbusPacket(1, Inputs.Address.Value, 1)

    Outputs.Result.Value = False
    if result[0] == True:
        Outputs.Result.Value = True

def __outputs__():
    Outputs.Result = new.bool(False)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
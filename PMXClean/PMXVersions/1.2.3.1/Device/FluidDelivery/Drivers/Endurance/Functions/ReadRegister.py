#DisplayName = Read Register
#Description = Reads a single register from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    #Description = The Address of the register to read from
    Inputs.Address = new.int(20000)

def __run__():
    result = SendAndReceiveModbusPacket(3, Inputs.Address.Value, 1)
    Outputs.Result.Value = result[0]

def __outputs__():
    Outputs.Result = new.int(-1)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
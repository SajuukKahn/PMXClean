#DisplayName = Write Coil
#Description = Writes to a single coil from the Unitronics controller
#Icon = NotebookEditOutlineMaterialIcon

def __inputs__():
    #Description = The address of the coil to write to
    Inputs.Address = new.int(20000)

    #Description = The value to write to the coil
    Inputs.Argument = new.bool(False)

def __run__():
    value = 0
    if Inputs.Argument.Value == True:
        value = 1

    SendAndReceiveModbusPacket(6, Inputs.Address.Value, value)

def __outputs__():
    pass

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
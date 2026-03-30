#DisplayName = Write Register
#Description = Writes to a single register from the Unitronics controller
#Icon = NotebookEditOutlineMaterialIcon

def __inputs__():
    #Description = The address of the register to write to
    Inputs.Address = new.int(20000)

    #Description = The value to write to the register
    Inputs.Argument = new.int(0)

def __run__():
    SendAndReceiveModbusPacket(6, Inputs.Address.Value, Inputs.Argument.Value)

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
#DisplayName = Execute Command
#Description = Execute a raw Galil command from the terminal
#Icon = SendMaterialIcon

def __inputs__():
    #Description = The command to send to the Galil
    Inputs.Command = new.string("TP")

def __run__():
    try:
        sendcommand()
    except:
        return

def __virtual__():
    pass

def sendcommand():
    response = parseresponse(SendAndReceive(str(Inputs.Command.Value), False))
    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

    Outputs.Response.Value = response
    return response

def parseresponse(command):
    if command is not None:
        return command.rstrip(' :\t\r\n\0')
    return command

def __outputs__():
    #Description = The response from the command sent, with any whitespace or colons stripped out
    Outputs.Response = new.string("null")

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
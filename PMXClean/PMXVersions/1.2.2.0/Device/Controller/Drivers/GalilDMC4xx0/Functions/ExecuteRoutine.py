#DisplayName = Execute Routine
#Description = Execute a routine in the Galil from a known label name
#Icon = SendMaterialIcon

def __inputs__():
    #Description = The label name to execute, including the # symbol
    Inputs.Routine = new.string("#INIT")

    #Description = The thread to execute the Routine on
    Inputs.Thread = new.int(1, 0, 7, 1, 1, "")
    
    #DisplayName = Wait for End
    #Description = A value indicating whether to await the completion of the created thread
    Inputs.WaitForEnd = new.bool(False)

def __run__():
    thread = int(Inputs.Thread.Value)
    SendAndReceive("HX" + str(thread), False)
    response = SendAndReceive("XQ" + str(Inputs.Routine) + "," + str(int(thread)), False)
    if response is None:
        __throwexception__(Exceptions.NoResponse)

    if Inputs.WaitForEnd.Value:
        WaitThreadComplete(thread)

def __virtual__():
    pass

def __outputs__():
    pass

def parseresponse(command):
    return command.split("\r\n")[0].strip()

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
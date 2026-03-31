#DisplayName = Trigger Off
#Description = Manually turn off the scanner trigger when running continuous
#Icon = FlashOffMaterialIcon
#Flags = IsHidden

def __inputs__():
    pass

def __run__():
    SendPacket("TRIGGER OFF")

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

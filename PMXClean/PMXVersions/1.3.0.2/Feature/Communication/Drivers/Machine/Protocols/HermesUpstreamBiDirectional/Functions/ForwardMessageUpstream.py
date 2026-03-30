#DisplayName = Forward Message Upstream
#Description = Gets message from server upstream message queue and sends it on the primary connection.
#Icon = ChevronTripleLeftMaterialIcon
#Flags = IsHidden, IsPolling

def __inputs__():
    pass

def __run__():
    if Settings.SupervisoryConnection is not None:
        msgToFwd = Settings.SupervisoryConnection.DequeueUpstreamMessage()
        if msgToFwd is not None and msgToFwd != "":
            Send(msgToFwd)

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
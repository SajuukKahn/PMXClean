#DisplayName = Reverse Transfer Status
#Description = The reverse transfer statuses of this Hermes connection
#Icon = ListStatusMaterialIcon
#Flags = IsHidden

def __inputs__():
    pass

def __run__():
    pass

def __virtual__():
    pass

def __outputs__():
    #Property = True
    #DisplayName = Machine Ready
    #Description = A value indicating whether or not the adjacent machine is ready to receive a part.
    Outputs.IsMachineReady = new.bool(False, True)

    #Property = True
    #DisplayName = Board Available
    #Description = A value indicating whether or not the local machine has a part to send.
    Outputs.IsBoardAvailable = new.bool(False, True)

    #Property = True
    #DisplayName = Transferring
    #Description = A value indicating whether or not a part is currently being transferred.
    Outputs.IsTransferring = new.bool(False, True)

def __exceptions__():
    pass
    
def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
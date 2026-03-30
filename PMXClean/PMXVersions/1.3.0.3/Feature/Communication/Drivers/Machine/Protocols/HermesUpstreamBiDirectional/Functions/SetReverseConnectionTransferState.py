#DisplayName = Set Reverse Connection Transfer State
#Description = Manually set status of machine reverse transfer
#Icon = ListStatusMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

def __inputs__():
    #Optional = True
    Inputs.MachineReady = new.bool(False)
    
    #Optional = True
    Inputs.BoardAvailable = new.bool(False)
    
    #Optional = True
    Inputs.Transferring = new.bool(False)

def __run__():
    if Inputs.MachineReady is not None:
        _ReverseTransferStatus_.IsMachineReady.Value = Inputs.MachineReady.Value

    if Inputs.BoardAvailable is not None:
        _ReverseTransferStatus_.IsBoardAvailable.Value = Inputs.BoardAvailable.Value

    if Inputs.Transferring is not None:
        _ReverseTransferStatus_.IsTransferring.Value = Inputs.Transferring.Value

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
#DisplayName = Read Right Material Low
#Description = Reads the right material low value from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    rightMaterialLowAddress = new.int(21003)
    result = ReadCoil(rightMaterialLowAddress)
    Outputs.RightMaterialLow.Value = result.Result.Value

def __outputs__():
    Outputs.RightMaterialLow = new.bool(False, True)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
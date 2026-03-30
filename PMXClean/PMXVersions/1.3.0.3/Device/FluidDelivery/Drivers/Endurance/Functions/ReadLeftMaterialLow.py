#DisplayName = Read Left Material Low
#Description = Reads the left material low value from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    leftMaterialLowAddress = new.int(21001)
    result = ReadCoil(leftMaterialLowAddress)
    Outputs.LeftMaterialLow.Value = result.Result.Value

def __outputs__():
    Outputs.LeftMaterialLow = new.bool(False, True)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
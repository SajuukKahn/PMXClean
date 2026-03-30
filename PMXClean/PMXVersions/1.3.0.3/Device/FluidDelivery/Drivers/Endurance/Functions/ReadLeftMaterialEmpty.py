#DisplayName = Read Left Material Empty
#Description = Reads the left material empty value from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    leftMaterialEmptyAddress = new.int(21002)
    result = ReadCoil(leftMaterialEmptyAddress)
    Outputs.LeftMaterialEmpty.Value = result.Result.Value

def __outputs__():
    Outputs.LeftMaterialEmpty = new.bool(False, True)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
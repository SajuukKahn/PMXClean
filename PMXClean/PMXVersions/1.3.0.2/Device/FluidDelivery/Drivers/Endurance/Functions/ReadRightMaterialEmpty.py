#DisplayName = Read Right Material Empty
#Description = Reads the right material empty value from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    rightMaterialEmptyAddress = new.int(21003)
    result = ReadCoil(rightMaterialEmptyAddress)
    Outputs.RightMaterialEmpty.Value = result.Result.Value

def __outputs__():
    Outputs.RightMaterialEmpty = new.bool(False, True)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
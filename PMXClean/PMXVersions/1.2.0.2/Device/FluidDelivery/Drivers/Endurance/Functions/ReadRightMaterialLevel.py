#DisplayName = Read Right Material Level
#Description = Reads the right material level from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    rightMaterialAddress = new.int(20004)
    result = ReadRegister(rightMaterialAddress)
    Outputs.Index.Value = result.Result.Value

def __outputs__():
    Outputs.MaterialLevel = new.int(-1)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
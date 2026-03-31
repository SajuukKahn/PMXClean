#DisplayName = Read Left Material Level
#Description = Reads the left material level from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    leftMaterialAddress = new.int(20003)
    result = ReadRegister(leftMaterialAddress)
    Outputs.MaterialLevel.Value = result.Result.Value

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
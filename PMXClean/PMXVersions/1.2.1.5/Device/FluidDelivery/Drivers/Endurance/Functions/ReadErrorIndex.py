#DisplayName = Read Error Index
#Description = Reads the error index from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    errorIndexAddress = new.int(20001)
    result = ReadRegister(errorIndexAddress)

    errorCode = result.Result.Value

    if (errorCode > 60000):
        errorCode = -1

    Outputs.ErrorIndex.Value = errorCode

def __outputs__():
    Outputs.ErrorIndex = new.int(-1)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
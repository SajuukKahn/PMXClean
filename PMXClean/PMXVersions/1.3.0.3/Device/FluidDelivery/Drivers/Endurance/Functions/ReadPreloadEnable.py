#DisplayName = Read Preload Enable
#Description = Reads the preload enable value from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    preloadEnableAddress = new.int(21000)
    result = ReadCoil(preloadEnableAddress)
    Outputs.PreloadEnable.Value = result.Result.Value

def __outputs__():
    Outputs.PreloadEnable = new.bool(False, True)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
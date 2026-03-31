#DisplayName = Write Preload Enable
#Description = Writes the preload enable value to the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    #DisplayName = Preload Enable
    #Description = Sets a value indicating whether to preload pressure before dispensing
    Inputs.PreloadEnable = new.bool(False)

def __run__():
    preloadEnableAddress = new.int(21000)
    WriteCoil(preloadEnableAddress, Inputs.PreloadEnable)

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
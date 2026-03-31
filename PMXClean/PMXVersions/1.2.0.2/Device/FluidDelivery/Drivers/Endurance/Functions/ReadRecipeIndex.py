#DisplayName = Read Recipe Index
#Description = Reads the recipe index from the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    recipeIndexAddress = new.int(20000)
    result = ReadRegister(recipeIndexAddress)
    Outputs.Index.Value = result.Result.Value

def __outputs__():
    Outputs.Index = new.int(-1)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
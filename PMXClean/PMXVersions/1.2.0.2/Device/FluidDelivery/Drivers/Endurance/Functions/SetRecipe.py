#DisplayName = Set Recipe
#Description = Writes the recipe index to the Unitronics controller.
#Icon = BookOpenVariantMaterialIcon
#Flags = IsProgramStep, IsTriggerStep

def __inputs__():
    #Description = The index of the recipe to set
    Inputs.Index = new.int(0, 0, 99, 1, 10, "")

def __run__():
    recipeIndexAddress = new.int(20000)
    WriteRegister(recipeIndexAddress, Inputs.Index)

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
#DisplayName = Refill
#Description = Set the refill output and wait the complete input. Has a 5 minute timeout
#Icon = WaterPlusOutlineMaterialIcon
#Flags = IsProgramStep, IsTriggerStep

def __inputs__():
    #DisplayName = Set Recipe
    #Description = A value indicating whether to set the recipe on the cart for this refill
    Inputs.SetRecipe = new.bool(False)

    #DisplayName = Recipe Index
    #Description = The index of the recipe to select if Set Recipe is true
    Inputs.RecipeIndex = new.int(1)

def __run__():
    if (Settings.CycleStart is None):
        __throwexception__(Exceptions.CycleStartMissing)
        return

    if (Settings.CycleComplete is None):
        __throwexception__(Exceptions.CycleCompleteMissing)
        return

    if Inputs.SetRecipe.Value:
        WriteRecipeIndex(Inputs.RecipeIndex.Value)

    Settings.Refill.Set(True)
    StartMonitoring()

    complete = Settings.CycleComplete.Value
    timeout = PVA.System.GetCurrentTime().Value + 300000
    while (complete is False) and (PVA.System.GetCurrentTime().Value < timeout):
        complete = Settings.CycleComplete.Value
        PVA.System.Wait(10)

    StopMonitoring()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.CycleStartMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.CycleStartMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.CycleCompleteMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#FluidDelivery.Exceptions.CycleCompleteMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
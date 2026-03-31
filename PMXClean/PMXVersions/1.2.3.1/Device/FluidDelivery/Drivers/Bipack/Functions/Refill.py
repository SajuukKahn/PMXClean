#DisplayName = Refill
#Description = Refill the bipack rods
#Icon = DoubleArrowUpThinMaterialIcon
#Flags = IsQuickAction

dialogName = "BipackRefill"

def __inputs__():
    pass

def __run__():
    global dialogName

    if Settings.RefillAirOutput is None:
        __throwexception__(Exceptions.RefillAirOutputMissing)
        return

    if Settings.DispenseAirOutput is None:
        __throwexception__(Exceptions.DispenseAirOutputMissing)
        return

    if AlwaysOn():
        Settings.DispenseAirOutput.Set(False)

    Settings.RefillAirOutput.Set(True)
    PVA.System.Wait(1000)
    Settings.RefillAirOutput.Set(False)

    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, "#FluidDelivery.BipackTitle")
    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#UI.Continue", None)
    PVA.Messaging.SetDialogMessageWithParameters(dialogName, "#FluidDelivery.BipackRefill", GetDisplayName())

    PVA.Messaging.ShowDialogAsync(dialogName)

    while not PVA.Messaging.CheckDialogInteraction(dialogName):
        PVA.System.Wait(25)

    PVA.Messaging.CloseDialog(dialogName)

    if AlwaysOn():
        Settings.DispenseAirOutput.Set(True)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.RefillAirOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.RefillAirOutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.DispenseAirOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#FluidDelivery.Exceptions.DispenseAirOutputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
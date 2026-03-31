#DisplayName = Read
#Description = Read a barcode from the scanner
#Icon = BookOpenMaterialIcon

dialogName = None
cancelled = False

def __inputs__():
    #DisplayName = Show Status Message
    #Description = A value indicating whether the function should show a message to the user while waiting to scan
    Inputs.ShowStatusMessage = new.bool(True)

def __run__():
    global dialogName
    global cancelled
    dialogName = None
    cancelled = False

    ClearLastBarcode()
    barcode = None

    if Inputs.ShowStatusMessage.Value:
        dialogName = PVA.Messaging.CreateUniqueDialog()
        PVA.Messaging.SetDialogIcon(dialogName, "BarcodeScanMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
        PVA.Messaging.SetDialogTitle(dialogName, GetDisplayName())
        PVA.Messaging.SetDialogMessageWithParameters(dialogName, "#Barcode.ScanBarcode", GetDisplayName())
        PVA.Messaging.SetDialogButtonProperties(dialogName, 0, True, True, True, "#UI.Cancel", cancel)
        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
        PVA.Messaging.ShowDialogAsync(dialogName)

    while barcode is None and not cancelled:
        PVA.System.Wait(50)
        barcode = GetLastBarcode()

    if cancelled:
        Outputs.Barcode.Value = "null"
        __throwexception__(Exceptions.ScanTimeout)
        return

    if barcode is None:
        Outputs.Barcode.Value = "null"
        __throwexception__(Exceptions.ScanTimeout)
        return

    Outputs.Barcode.Value = barcode

    if dialogName is not None:
        PVA.Messaging.CloseDialog(dialogName)
        dialogName = None

def __virtual__():
    pass

def __outputs__():
    Outputs.Barcode = new.string("null")

def __exceptions__():
    Exceptions.ScanTimeout = new.exception("#Barcode.Exceptions.ScanBarcodeTimeoutTitle", "#Barcode.Exceptions.ScanBarcodeTimeout", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    global dialogName
    if (dialogName is not None):
        PVA.Messaging.CloseDialog(dialogName)
        dialogName = None

def __exceptionrecovery__():
    pass

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def cancel():
    global cancelled
    cancelled = True
#DisplayName = Read
#Description = Read a barcode from the scanner
#Icon = BookOpenMaterialIcon

dialogName = None

def __inputs__():
    #DisplayName = Show Status Message
    #Description = A value indicating whether the function should show a message to the user while waiting to scan
    Inputs.ShowStatusMessage = new.bool(False)

def __run__():
    global dialogName

    if Inputs.ShowStatusMessage.Value:
        dialogName = PVA.Messaging.CreateUniqueDialog()
        PVA.Messaging.SetDialogIcon(dialogName, "BarcodeScanMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
        PVA.Messaging.SetDialogTitle(dialogName, GetDisplayName())
        PVA.Messaging.SetDialogMessageWithParameters(dialogName, "#Barcode.ScanningBarcode", GetDisplayName())
        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
        PVA.Messaging.ShowDialogAsync(dialogName)

    response = SendAndReceive("TRIGGER ON", False)

    if response is None:
        Outputs.Barcode.Value = "null"
        __throwexception__(Exceptions.BadResponse)
        return

    barcodes = ParseResponse(response, Settings.Delimiter.Value, Settings.Header.Value, Settings.Footer.Value)
    barcode = barcodes[0]

    if barcode is None or barcode is "":
        Outputs.Barcode.Value = "null"
        __throwexception__(Exceptions.ReadTimeout)
        return

    Outputs.Barcode.Value = barcode

    if dialogName is not None:
        PVA.Messaging.CloseDialog(dialogName)
        dialogName = None

def __virtual__():
    pass

def __outputs__():
    #Property = true
    #Description = The barcode string that was read
    Outputs.Barcode = new.string("null")

def __exceptions__():
    Exceptions.BadResponse = new.exception("#Connection.Exceptions.BadResponseTitle", "#Connection.Exceptions.BadResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.ReadTimeout = new.exception("#Connection.Exceptions.ReadTimeoutTitle", "#Connection.Exceptions.ReadTimeout", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    TriggerOff()
    global dialogName
    if (dialogName is not None):
        PVA.Messaging.CloseDialog(dialogName)
        dialogName = None

def __exceptionrecovery__():
    pass
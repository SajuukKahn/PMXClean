#DisplayName = Poll Read
#Description = Polls the barcode reading from the hand scanner
#Icon = FlashOffMaterialIcon
#Flags = IsPolling, IsHidden

def __inputs__():
    pass

def __run__():
    barcodes = GetBarcodeResults(Settings.Delimiter.Value, Settings.Header.Value, Settings.Footer.Value)
    if barcodes is not None:
        if len(barcodes) > 0 and barcodes[-1] != Settings.NoRead.Value:
            Outputs.Barcode.Value = barcodes[-1]

        Outputs.IsCurrent.Value = Outputs.Barcode.Value == GetLastBarcode()

def __virtual__():
    pass

def __outputs__():
    #Property = true
    #Description = The barcode string that was last read
    Outputs.Barcode = new.string("null")

    #Property = true
    #Description = A value indicating whether the barcode string is current
    Outputs.IsCurrent = new.bool(False, True)

def __exceptions__():
    pass

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

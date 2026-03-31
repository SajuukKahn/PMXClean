# DisplayName = Read
# Description = Read a barcode from the scanner
# Icon = BookOpenMaterialIcon

def __inputs__():
    pass

def __run__():
    response = SendAndReceive("TRIGGER ON", False)

    if response is None:
        Outputs.Barcode.Value = "null"
        __throwexception__(Exceptions.BadResponse)
        return

    barcodes = ParseResponse(response, Settings.Delimiter.Value, Settings.Header.Value, Settings.Footer.Value)

    if barcodes is None or barcodes[0] is "":
        Outputs.Barcode.Value = "null"
        __throwexception__(Exceptions.ReadTimeout)
        return

    Outputs.Barcode.Value = barcodes[0]

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

def __exceptionrecovery__():
    pass

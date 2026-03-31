# DisplayName = Select Product
# Description = Select a product using a barcode read from the scanner and existing product identifiers
# Icon = BookOpenMaterialIcon

def __inputs__():
    #DisplayName = Substring Start Index
    #Description = The starting index of the substring of read string to compare against product identifiers
    Inputs.SubstringStartIndex = new.int(0, 0, 5000, 1, 1, "")

    #Optional = True
    #Enabled = False
    #DisplayName = Substring Length
    #Description = The length of the substring of the read string to compare against product identifiers
    Inputs.SubstringLength = new.int(15, 1, 5000, 1, 1, "")

def __run__():
    if Inputs.SubstringLength is None:
        substringlength = -1
    else:
        substringlength = Inputs.SubstringLength.Value

    readResult = Read().Barcode

    if (Inputs.SubstringStartIndex.Value > len(readResult.Value)):
        __throwexception__(Exceptions.InvalidStartingIndex)

    if (substringlength > (len(readResult.Value) - Inputs.SubstringStartIndex.Value)):
        __throwexception__(Exceptions.InvalidSubstringLength)

    if not SelectProductByBarcode(readResult.Value, Inputs.SubstringStartIndex.Value, substringlength):
        Exceptions.FailedToSelectProduct.ExceptionData.MessageParams = tuple([readResult.Value])
        __throwexception__(Exceptions.FailedToSelectProduct)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.InvalidStartingIndex = new.exception("#Barcode.Exceptions.InvalidStartingIndexTitle", "#Barcode.Exceptions.InvalidStartingIndex", new.enum("Severity", "Error").Value, None)
    Exceptions.InvalidSubstringLength = new.exception("#Barcode.Exceptions.InvalidSubstringLengthTitle", "#Barcode.Exceptions.InvalidSubstringLength", new.enum("Severity", "Error").Value, None)
    Exceptions.FailedToSelectProduct = new.exception("#Barcode.Exceptions.FailedToSelectProductTitle", "#Barcode.Exceptions.FailedToSelectProduct", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    TriggerOff()

def __exceptionrecovery__():
    pass
#DisplayName = Select Product
#Description = Select a product based on the next barcode read from the scanner
#Icon = BookOpenMaterialIcon

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

    readResult = Read(new.bool(True)).Barcode

    if (Inputs.SubstringStartIndex.Value > len(readResult.Value)):
        __throwexception__(Exceptions.InvalidStartingIndex)

    if (substringlength > (len(readResult.Value) - Inputs.SubstringStartIndex.Value)):
        __throwexception__(Exceptions.InvalidSubstringLength)

    productName = PVA.Product.GetProductNameByID(readResult.Value, Inputs.SubstringStartIndex.Value, substringlength)
    if productName is None or not PVA.Product.SelectProductByName(productName):
        Exceptions.FailedToSelectProduct.ExceptionData.MessageParams = tuple([readResult.Value])
        __throwexception__(Exceptions.FailedToSelectProduct)

    Outputs.Barcode.Value = readResult.Value

def __virtual__():
    pass

def __outputs__():
    #Description = The barcode string that was read
    Outputs.Barcode = new.string("null")

def __exceptions__():
    Exceptions.InvalidStartingIndex = new.exception("#Barcode.Exceptions.InvalidStartingIndexTitle", "#Barcode.Exceptions.InvalidStartingIndex", new.enum("Severity", "Error").Value, None)
    Exceptions.InvalidSubstringLength = new.exception("#Barcode.Exceptions.InvalidSubstringLengthTitle", "#Barcode.Exceptions.InvalidSubstringLength", new.enum("Severity", "Error").Value, None)
    Exceptions.FailedToSelectProduct = new.exception("#Barcode.Exceptions.FailedToSelectProductTitle", "#Barcode.Exceptions.FailedToSelectProduct", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
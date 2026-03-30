#DisplayName = Select Product from Board Data
#Description = Select a product based on the current Hermes Board Data
#Icon = BookOpenMaterialIcon
#Flags = IsProcessStep

import xml.etree.ElementTree as ET

def __inputs__():
    #DisplayName = Message Field
    #Description = The BoardAvailable data field to use for Product Selection
    Inputs.MessageField = new.enum("HermesBoardAttributes", "TopBarcode")
    
    #CanReference = True
    #DisplayName = Substring Start Index
    #Description = The starting index of the substring of read string to compare against product identifiers
    Inputs.SubstringStartIndex = new.int(0, 0, 5000, 1, 1, "")

    #CanReference = True
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

    dataFieldValue = getXMLAttribValueFromString(GetBufferedMessage(), "BoardAvailable", str(Inputs.MessageField.Value))

    if (Inputs.SubstringStartIndex.Value > len(dataFieldValue)):
        __throwexception__(Exceptions.InvalidStartingIndex)

    if (substringlength > (len(dataFieldValue) - Inputs.SubstringStartIndex.Value)):
        __throwexception__(Exceptions.InvalidSubstringLength)

    productName = PVA.Product.GetProductNameByID(dataFieldValue, Inputs.SubstringStartIndex.Value, substringlength)
    if productName is None or not PVA.Product.SelectProductByName(productName):
        Exceptions.FailedToSelectProduct.ExceptionData.MessageParams = tuple([dataFieldValue])
        __throwexception__(Exceptions.FailedToSelectProduct)

def getXMLAttribValueFromString(xmlStringMsg, msgName, attribName):
    try:
        xmlMsgTree = ET.fromstring(xmlStringMsg)
    except:
        return ""
    msgNode = xmlMsgTree.find(msgName)
    if msgNode is not None:
        return msgNode.get(attribName, "")
    else:
        return ""

def __outputs__():
    pass

def __exceptions__():
    Exceptions.InvalidStartingIndex = new.exception("#Communication.Exceptions.InvalidStartingIndexTitle", "#Communication.Exceptions.InvalidStartingIndex", new.enum("Severity", "Error").Value, None)
    Exceptions.InvalidSubstringLength = new.exception("#Communication.Exceptions.InvalidSubstringLengthTitle", "#Communication.Exceptions.InvalidSubstringLength", new.enum("Severity", "Error").Value, None)
    Exceptions.FailedToSelectProduct = new.exception("#Communication.Exceptions.FailedToSelectProductTitle", "#Communication.Exceptions.FailedToSelectProduct", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    WriteToLog(exception.ExceptionData.FormattedMessage)
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
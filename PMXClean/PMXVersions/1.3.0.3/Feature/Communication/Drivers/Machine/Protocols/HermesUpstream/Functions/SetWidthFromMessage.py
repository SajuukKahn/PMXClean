#DisplayName = Set Width From Message
#Description = Set the width of the servo adjust based on the current Hermes BoardAvailable message
#Icon = ArrowLeftRightMaterialIcon
#Flags = IsProcessStep

import xml.etree.ElementTree as ET

def __inputs__():
    Inputs.Conveyor = new.device("Conveyor", 0)

    Inputs.Offset = new.double(0, 0, 1000, 1, 10, "mm")
    
    #Description = A value indicating whether to execute the PreAdjust trigger
    Inputs.PreAdjust = new.bool(False)

    #Description = A value indicating whether to execute the PostAdjust trigger
    Inputs.PostAdjust = new.bool(False)

def __run__():
    if Inputs.Conveyor is None:
        __throwexception__(Exceptions.InputMissing)
        return

    productWidth = getXMLAttribValueFromString(GetBufferedMessage(), "BoardAvailable", "Width")

    if productWidth == "":
        __throwexception__(Exceptions.ProductMissingProperty, "Width")
        return

    Inputs.Conveyor.SetWidth(new.int(Inputs.Conveyor.ConvertMeasurementToCounts(float(productWidth) + Inputs.Offset.Value), 0, 500000, 1, 10, "mm"), Inputs.PreAdjust, Inputs.PostAdjust)

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

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ProductMissingProperty = new.exception("#Communication.Exceptions.WidthPropertyMissingTitle", "#Communication.Exceptions.WidthPropertyMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.InputMissing = new.exception("#Scripting.Exceptions.ScriptValueRequiredTitle", "#Scripting.Exceptions.ScriptValueRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
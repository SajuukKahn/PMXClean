#DisplayName = Send Hermes Capabilities Message
#Description = Sends description of Hermes capabilities to supervisory system.
#Icon = NotebookOutlineMaterialIcon
#Flags = IsHidden

import xml.etree.ElementTree as ET

def __inputs__():
    Inputs.ConnectionToSendOn = new.int(1, 1, 2, 1, 1, "")

def __run__():
    if Settings.EquipID is None or Settings.EquipID.Value == "":
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    if Settings.LaneID is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return
    
    msgToSend = buildMessage()
    if Inputs.ConnectionToSendOn.Value == 1:
        if not Send(msgToSend):
            __throwexception__(Exceptions.SendError)
            return

    if Inputs.ConnectionToSendOn.Value == 2 and IsSecondConnectionSet():
        if not SendSecondConnection(msgToSend):
            __throwexception__(Exceptions.SendError)
            return

def buildMessage():
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", GetTimestamp().Timestamp.Value)
    msgChild = ET.SubElement(hermesRoot, "SendHermesCapabilities")

    messagesNode = ET.SubElement(msgChild, "OptionalMessages")
    boardForecastNode = ET.SubElement(messagesNode, "MessageBoardForecast")
    commandNode = ET.SubElement(messagesNode, "MessageCommand")

    #From Hermes 1.6 Specification Document
    #The type of support of attributes is encoded bit-wise:
    #1 - ‘p’ machine passes on attribute or ‘-’ if it does not pass it on
    #2 - ‘u’ machine updates attribute or ‘-’ if it does not update
    #4 - ‘r’ machine reacts to attribute or ‘-’ if it does not react
    #Examples:
    #[--p] Pass on attribute -> 1
    #[r-p] React on attribute and pass on attribute -> 5
    #[rup] React and update attribute and send updated attribute -> 7

    attributesNode = ET.SubElement(msgChild, "Attributes")
    attributesNode.set("ProductTypeId", "5")
    attributesNode.set("TopBarcode", "5")
    attributesNode.set("BottomBarcode", "5")
    attributesNode.set("Length", "1")
    attributesNode.set("Width", "5")
    attributesNode.set("Thickness", "1")
    attributesNode.set("ConveyorSpeed", "5")
    attributesNode.set("TopClearanceHeight", "1")
    attributesNode.set("BottomClearanceHeight", "1")
    attributesNode.set("Weight", "1")
    attributesNode.set("WorkOrderId", "5")
    attributesNode.set("BatchId", "5")
    attributesNode.set("Route", "1")
    attributesNode.set("Action", "5")
    attributesNode.set("SubBoards", "5")
    
    return ET.tostring(hermesRoot).decode()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ConfigValueRequired = new.exception("#Scripting.Exceptions.ConfigValueRequiredTitle", "#Scripting.Exceptions.ConfigValueRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.SendError = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.SendError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    WriteToLog(exception.ExceptionData.FormattedMessage)
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
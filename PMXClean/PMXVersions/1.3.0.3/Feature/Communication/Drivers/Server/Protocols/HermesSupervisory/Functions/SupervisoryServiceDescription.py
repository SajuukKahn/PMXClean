#DisplayName = Supervisory Service Description Message
#Description = Sends description of Hermes implementation to supervisory system.
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
    msgChild = ET.SubElement(hermesRoot, "SupervisoryServiceDescription")
    msgChild.set("SystemId", Settings.EquipID.Value)
    msgChild.set("Version", "1.6")
    featuresNode = ET.SubElement(msgChild, "SupportedFeatures")
    boardForecastNode = ET.SubElement(featuresNode, "FeatureBoardForecast")
    commandNode = ET.SubElement(featuresNode, "FeatureCommand")
    
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
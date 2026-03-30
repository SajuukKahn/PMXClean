#DisplayName = Transport Finished
#Description = Signal the downstream machine that PCB transport is finished.
#Icon = RayStartEndMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

import xml.etree.ElementTree as ET

def __inputs__():
    #CanReference = True
    #Description = Transport Status 1 - Not Started, 2 - Incomplete, 3 - Complete
    Inputs.TransferState = new.int(3, 1, 3, 1, 1, "")

def __run__():
    if Settings.SupervisoryConnection is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    if Inputs.TransferState is None:
        __throwexception__(Exceptions.InputMissing)
        return

    _TransferStatus_.IsBoardAvailable.Value = False
    if not Send(buildMessage()):
        __throwexception__(Exceptions.SendError)
        return

def buildMessage():
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", Settings.SupervisoryConnection.GetTimestamp().Timestamp.Value)
    msgChild = ET.SubElement(hermesRoot, "TransportFinished")
    msgChild.set("TransferState", str(int(Inputs.TransferState.Value)))
    msgChild.set("BoardId", getBufferedBoardId())
    
    return ET.tostring(hermesRoot).decode()

def getBufferedBoardId():
    try:
        xmlMsgTree = ET.fromstring(GetBufferedMessage())
    except:
        return ""
    msgNode = xmlMsgTree.find("BoardAvailable")
    if msgNode is not None:
        return msgNode.get("BoardId", "")
    else:
        return ""

def __outputs__():
    pass

def __exceptions__():
    Exceptions.InputMissing = new.exception("#Scripting.Exceptions.ScriptValueRequiredTitle", "#Scripting.Exceptions.ScriptValueRequired", new.enum("Severity", "Error").Value, None)
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
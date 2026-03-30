#DisplayName = Revoke Board Available
#Description = Notify downstream machine that a board is no longer available to be sent.
#Icon = CommentCheckOutlineMaterialIcon
#SubIcon = CloseOctagonMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

import xml.etree.ElementTree as ET

def __inputs__():
    pass

def __run__():
    if Settings.SupervisoryConnection is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    _TransferStatus_.IsBoardAvailable.Value = False
    if not Send(buildMessage()):
        __throwexception__(Exceptions.SendError)
        return

def buildMessage():
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", Settings.SupervisoryConnection.GetTimestamp().Timestamp.Value)
    msgChild = ET.SubElement(hermesRoot, "RevokeBoardAvailable")
    
    return ET.tostring(hermesRoot).decode()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.SendError = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.SendError", new.enum("Severity", "Error").Value, None)
    Exceptions.ConfigValueRequired = new.exception("#Scripting.Exceptions.ConfigValueRequiredTitle", "#Scripting.Exceptions.ConfigValueRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    WriteToLog(exception.ExceptionData.FormattedMessage)
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = Service Description Message
#Description = Sends description of Hermes implementation to adjacent machine.
#Icon = NotebookOutlineMaterialIcon
#Flags = IsHidden

import xml.etree.ElementTree as ET

def __inputs__():
    pass

def __run__():
    if Settings.SupervisoryConnection is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    configData = Settings.SupervisoryConnection.GetConfigurationData()
    
    if configData.EquipID is None or configData.EquipID.Value == "":
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    if configData.LaneID is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return
    
    msgToSend = Settings.SupervisoryConnection.GetServiceDescriptionMessage().Message.Value
    if not Send(msgToSend):
        __throwexception__(Exceptions.SendError)
        return

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
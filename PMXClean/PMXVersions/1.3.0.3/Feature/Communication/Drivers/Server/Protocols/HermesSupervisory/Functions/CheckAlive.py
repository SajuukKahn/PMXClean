#DisplayName = Check Alive Message
#Description = Sends message to connected supervisory station to verify connectivity.
#Icon = PollMaterialIcon
#Flags = IsHidden, IsPolling

import xml.etree.ElementTree as ET

checkAliveTime = new.int(0)
exceptionThrown = True

def __inputs__():
    pass

def __run__():
    global checkAliveTime
    global exceptionThrown

    configData = GetConfigurationData()
    
    if configData.CheckAliveFrequency is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return
    
    if (PVA.System.GetCurrentTime().Value >= checkAliveTime.Value):
        msgToSend = buildMessage()
        if IsRemoteClientConnected():
            if not Send(msgToSend):
                if not exceptionThrown:
                    ResetConnection()
                    exceptionThrown = True
                    throwNotConnectedException(configData.CheckAliveErrorReporting)
            else:
                exceptionThrown = False
        elif not exceptionThrown:
            ResetConnection()
            exceptionThrown = True
            throwNotConnectedException(configData.CheckAliveErrorReporting)
        
        checkAliveTime.Value = PVA.System.GetCurrentTime().Value + configData.CheckAliveFrequency.Value

def buildMessage():
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", GetTimestamp().Timestamp.Value)
    msgChild = ET.SubElement(hermesRoot, "CheckAlive")
    
    return ET.tostring(hermesRoot).decode()

def throwNotConnectedException(severity):
    if severity is None or str(severity) == "":
        __throwexception__(Exceptions.ClientNotConnectedError)
    elif str(severity) == "Error":
        __throwexception__(Exceptions.ClientNotConnectedError)
    elif str(severity) == "Notification":
        PVA.Notification.ShowNotification(new.enum("NotificationType", "Information").Value, "#Communication.Exceptions.ErrorTitle", "#Communication.Notifications.ConnectionLoss", GetDisplayName(), "", True, False, False)
        __throwexception__(Exceptions.ClientNotConnectedSilent)
    elif str(severity) == "Silent":
        __throwexception__(Exceptions.ClientNotConnectedSilent)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ConfigValueRequired = new.exception("#Scripting.Exceptions.ConfigValueRequiredTitle", "#Scripting.Exceptions.ConfigValueRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.ClientNotConnectedError = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.ClientNotConnected", new.enum("Severity", "Error").Value, None)
    Exceptions.ClientNotConnectedSilent = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.ClientNotConnected", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    WriteToLog(exception.ExceptionData.FormattedMessage)
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
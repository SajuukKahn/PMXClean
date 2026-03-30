#DisplayName = Check Alive Message Second Connection
#Description = Sends message to connected device to verify connectivity on second connection.
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

    if Settings.SupervisoryConnection is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    configData = Settings.SupervisoryConnection.GetConfigurationData()
    
    if configData.CheckAliveFrequency is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return
    
    if (GetIsSecondConnectionStarted() and PVA.System.GetCurrentTime().Value >= checkAliveTime.Value):
        msgToSend = buildMessage()
        if IsSecondRemoteClientConnected():
            if not SendSecondConnection(msgToSend):
                if not exceptionThrown:
                    ResetSecondConnection()
                    exceptionThrown = True
                    throwNotConnectedException(configData.CheckAliveErrorReporting)
            else:
                exceptionThrown = False
        elif not exceptionThrown:
            ResetSecondConnection()
            exceptionThrown = True
            throwNotConnectedException(configData.CheckAliveErrorReporting)
        
        checkAliveTime.Value = PVA.System.GetCurrentTime().Value + configData.CheckAliveFrequency.Value

def buildMessage():
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", Settings.SupervisoryConnection.GetTimestamp().Timestamp.Value)
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
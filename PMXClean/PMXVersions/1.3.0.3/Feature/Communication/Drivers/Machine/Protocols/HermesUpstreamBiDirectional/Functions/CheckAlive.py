#DisplayName = Check Alive Message
#Description = Sends message to connected device to verify connectivity.
#Icon = PollMaterialIcon
#Flags = IsHidden, IsPolling

import xml.etree.ElementTree as ET

checkAliveTime = new.int(0)
reconnectTime = 0
reconnectFrequency = 1000
exceptionThrown = False

def __inputs__():
    pass

def __run__():
    global checkAliveTime
    global reconnectTime
    global reconnectFrequency
    global exceptionThrown

    if Settings.SupervisoryConnection is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    configData = Settings.SupervisoryConnection.GetConfigurationData()
    
    if configData.CheckAliveFrequency is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return
    
    if (PVA.System.GetCurrentTime().Value >= checkAliveTime.Value and checkAliveTime.Value > 0):
        msgToSend = buildMessage()
        if not Send(msgToSend):
            ResetConnection()
            checkAliveTime.Value = PVA.System.GetCurrentTime().Value + reconnectFrequency
            if not exceptionThrown:
                exceptionThrown = True
                throwNotConnectedException(configData.CheckAliveErrorReporting)
        else:
            exceptionThrown = False
            checkAliveTime.Value = PVA.System.GetCurrentTime().Value + configData.CheckAliveFrequency.Value

    # Prevents CheckAlive from being ran immediately after connection
    if checkAliveTime.Value == 0:
        checkAliveTime.Value = PVA.System.GetCurrentTime().Value + configData.CheckAliveFrequency.Value

def buildMessage():
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", Settings.SupervisoryConnection.GetTimestamp().Timestamp.Value)
    msgChild = ET.SubElement(hermesRoot, "CheckAlive")
    
    return ET.tostring(hermesRoot).decode()

def throwNotConnectedException(severity):
    if severity is None or str(severity) == "":
        __throwexception__(Exceptions.NotConnectedError)
    elif str(severity) == "Error":
        __throwexception__(Exceptions.NotConnectedError)
    elif str(severity) == "Notification":
        PVA.Notification.ShowNotification(new.enum("NotificationType", "Information").Value, "#Communication.Exceptions.ErrorTitle", "#Communication.Notifications.ConnectionLoss", GetDisplayName(), "", True, False, False)
        __throwexception__(Exceptions.NotConnectedSilent)
    elif str(severity) == "Silent":
        __throwexception__(Exceptions.NotConnectedSilent)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ConfigValueRequired = new.exception("#Scripting.Exceptions.ConfigValueRequiredTitle", "#Scripting.Exceptions.ConfigValueRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.NotConnectedError = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.NotConnected", new.enum("Severity", "Error").Value, None)
    Exceptions.NotConnectedSilent = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.NotConnected", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    WriteToLog(exception.ExceptionData.FormattedMessage)
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
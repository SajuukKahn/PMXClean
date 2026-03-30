#DisplayName = Notification
#Description = Sends a message to a connected device.
#Icon = NoteTextOutlineMaterialIcon
#Flags = IsTriggerStep

import xml.etree.ElementTree as ET

def __inputs__():
    #DisplayName = Notification Code
    #Description = The numerical code of the notification
    Inputs.NotificationCode = new.int(1, 1, 65536, 1, 10, "")
    
    #DisplayName = Severity
    #Description = The serverity of the notification
    Inputs.Severity = new.int(1, 1, 4, 1, 1, "")
    
    #DisplayName = Description
    #Description = The description of the notification
    Inputs.Description = new.string("")

def __run__():
    if Inputs.NotificationCode is None or Inputs.Severity is None or Inputs.Description is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    if not IsConnectedToServer():
        __throwexception__(Exceptions.NotConnected)
        return

    if not Send(buildMessage()):
        __throwexception__(Exceptions.SendError)
        return

def buildMessage():
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", GetTimestamp().Timestamp.Value)
    msgChild = ET.SubElement(hermesRoot, "Notification")
    msgChild.set("NotificationCode", str(int(Inputs.NotificationCode.Value)))
    msgChild.set("Severity", str(int(Inputs.Severity.Value)))
    msgChild.set("Description", Inputs.Description.Value)
    
    return ET.tostring(hermesRoot).decode()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.NotConnected = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.NotConnected", new.enum("Severity", "Error").Value, None)
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
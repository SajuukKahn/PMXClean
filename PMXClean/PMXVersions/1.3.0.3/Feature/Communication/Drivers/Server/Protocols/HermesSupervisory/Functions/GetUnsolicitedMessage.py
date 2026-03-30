#DisplayName = Poll Unsolicited Message
#Description = Get Unsolicited messages sent by the adjacent machine.
#Icon = PollMaterialIcon
#Flags = IsHidden, IsPolling

import xml.etree.ElementTree as ET

def __inputs__():
    pass

def __run__():
    msgReceived = ReceiveString()
    if msgReceived is not None:
        try:
            xmlMsgTree = ET.fromstring(msgReceived)
        except:
            xmlMsgTree = None

        if xmlMsgTree is not None and xmlMsgTree.tag.upper() == "HERMES":
            hermesMsg = xmlMsgTree[0].tag.upper()

            if hermesMsg == "SUPERVISORYSERVICEDESCRIPTION":
                SupervisoryServiceDescription(new.int(1))

            elif hermesMsg == "QUERYHERMESCAPABILITIES":
                SendHermesCapabilities(new.int(1))
                
            elif hermesMsg == "CHECKALIVE":
                return

            elif hermesMsg == "NOTIFICATION":
                notificationNode = xmlMsgTree.find("Notification")
                notificationCode = notificationNode.get("NotificationCode", "")
                severity = notificationNode.get("Severity", "")
                description = notificationNode.get("Description", "")
                if notificationCode == "" or severity == "" or description == "":
                    WriteToLog("Notification data missing.")
                else:
                    if severity == "1" or severity == "2":
                        __throwexception__(new.exception("Hermes Notification", "Code: " + notificationCode + "\r\nSeverity: " + severity + "\r\nDescription: " + description, new.enum("Severity", "Error").Value, None))
                    elif severity == "3":
                        __throwexception__(new.exception("Hermes Notification", "Code: " + notificationCode + "\r\nSeverity: " + severity + "\r\nDescription: " + description, new.enum("Severity", "Warning").Value, None))
                    elif severity == "4":
                        PVA.Notification.ShowNotification(new.enum("NotificationType", "Information").Value, "Hermes Notification", "Code: " + notificationCode + ", Severity: " + severity + "\r\nDescription: " + description, GetDisplayName(), "", True, False, False)
                        __throwexception__(new.exception("Hermes Notification", "Code: " + notificationCode + "\r\nSeverity: " + severity + "\r\nDescription: " + description, new.enum("Severity", "Silent").Value, None))
                    else:
                        __throwexception__(new.exception("Hermes Notification", "Code: " + notificationCode + "\r\nInvalid Severity: " + severity + "\r\nDescription: " + description, new.enum("Severity", "Silent").Value, None))

            elif hermesMsg == "SETCONFIGURATION":
                Notification(new.int(4), new.int(2), new.string("Configuration Error: Remote Configuration Not Supported"))
            
            else:
                return
                #Invalid or unsupported messages are to be ignored

        elif xmlMsgTree is not None and xmlMsgTree.tag.upper() != "HERMES":
            Notification(new.int(1), new.int(2), new.string("Protocol Error: Non-Hermes Message Received"))
            ResetConnection()

        elif xmlMsgTree is None:
            Notification(new.int(1), new.int(2), new.string("Protocol Error: Invalid Data Received"))
            ResetConnection()

def __outputs__():
    pass

def __exceptions__():
    pass

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    WriteToLog(exception.ExceptionData.FormattedMessage)
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
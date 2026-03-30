#DisplayName = Poll Unsolicited Message (Bi-Directional)
#Description = Get Unsolicited messages sent by the adjacent machine.
#Icon = PollMaterialIcon
#Flags = IsHidden, IsPolling

import xml.etree.ElementTree as ET

def __inputs__():
    pass

def __run__():
    if IsSecondConnectionSet():
        msgReceived = ReceiveStringSecondConnection()
        if msgReceived is not None:
            try:
                xmlMsgTree = ET.fromstring(msgReceived)
            except:
                xmlMsgTree = None

            if xmlMsgTree is not None and xmlMsgTree.tag.upper() == "HERMES":
                hermesMsg = xmlMsgTree[0].tag.upper()

                if hermesMsg == "SERVICEDESCRIPTION":
                    ServiceDescription(new.int(2))

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

                elif hermesMsg == "MACHINEREADY":
                    if not _ReverseTransferStatus_.IsMachineReady.Value:
                        _ReverseTransferStatus_.IsMachineReady.Value = True
                    else:
                        NotificationSecondConnection(new.int(1), new.int(2), new.string("Protocol Error: Invalid Transition (MachineReady)"))
                        ResetSecondConnection()
                        __throwexception__(new.exception("Hermes Error", "Protocol Error: Received Invalid Transition (MachineReady)", new.enum("Severity", "Error").Value, None))

                elif hermesMsg == "REVOKEMACHINEREADY":
                    if  _ReverseTransferStatus_.IsMachineReady.Value:
                        _ReverseTransferStatus_.IsMachineReady.Value = False
                    else:
                        NotificationSecondConnection(new.int(1), new.int(2), new.string("Protocol Error: Invalid Transition (RevokeMachineReady)"))
                        ResetSecondConnection()
                        __throwexception__(new.exception("Hermes Error", "Protocol Error: Received Invalid Transition (RevokeMachineReady)", new.enum("Severity", "Error").Value, None))

                elif hermesMsg == "STARTTRANSPORT":
                    if not _ReverseTransferStatus_.IsTransferring.Value and _ReverseTransferStatus_.IsBoardAvailable.Value:
                        startTransportBoardId = getXMLAttribValueFromString(msgReceived, "StartTransport", "BoardId")
                        bufferedBoardId = getXMLAttribValueFromString(GetBufferedMessage(), "BoardAvailable", "BoardId")
                        if bufferedBoardId != startTransportBoardId:
                            NotificationSecondConnection(new.int(1), new.int(2), new.string("Protocol Error: BoardID Mismatch"))
                            ResetSecondConnection()
                        else:
                            _ReverseTransferStatus_.IsTransferring.Value = True
                    else:
                        NotificationSecondConnection(new.int(1), new.int(2), new.string("Protocol Error: Invalid Transition (StartTransport)"))
                        ResetSecondConnection()
                        __throwexception__(new.exception("Hermes Error", "Protocol Error: Received Invalid Transition (StartTransport)", new.enum("Severity", "Error").Value, None))

                elif hermesMsg == "STOPTRANSPORT":
                    if _ReverseTransferStatus_.IsTransferring.Value:
                        stopTransportBoardId = getXMLAttribValueFromString(msgReceived, "StopTransport", "BoardId")
                        bufferedBoardId = getXMLAttribValueFromString(GetBufferedMessage(), "BoardAvailable", "BoardId")
                        if bufferedBoardId != stopTransportBoardId:
                            NotificationSecondConnection(new.int(1), new.int(2), new.string("Protocol Error: BoardID Mismatch"))
                            ResetSecondConnection()
                        _ReverseTransferStatus_.IsTransferring.Value = False
                        _ReverseTransferStatus_.IsMachineReady.Value = False
                    else:
                        NotificationSecondConnection(new.int(1), new.int(2), new.string("Protocol Error: Invalid Transition (StopTransport)"))
                        ResetSecondConnection()
                        __throwexception__(new.exception("Hermes Error", "Protocol Error: Received Invalid Transition (StopTransport)", new.enum("Severity", "Error").Value, None))
                
                else:
                    return
                    #Invalid or unsupported messages are to be ignored

            elif xmlMsgTree is not None and xmlMsgTree.tag.upper() != "HERMES":
                NotificationSecondConnection(new.int(1), new.int(2), new.string("Protocol Error: Non-Hermes Message Received"))
                ResetSecondConnection()

            elif xmlMsgTree is None:
                NotificationSecondConnection(new.int(1), new.int(2), new.string("Protocol Error: Invalid Data Received"))
                ResetSecondConnection()

def getXMLAttribValueFromString(xmlStringMsg, msgName, attribName):
    try:
        xmlMsgTree = ET.fromstring(xmlStringMsg)
    except:
        return ""
    msgNode = xmlMsgTree.find(msgName)
    if msgNode is not None:
        return msgNode.get(attribName, "")
    else:
        return ""

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
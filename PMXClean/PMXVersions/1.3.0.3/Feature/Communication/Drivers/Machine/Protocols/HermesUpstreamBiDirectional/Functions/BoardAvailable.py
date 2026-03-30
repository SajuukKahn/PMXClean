#DisplayName = Board Available (Bi-Directional)
#Description = Notify adjacent machine that a board is available to be sent.
#Icon = CommentCheckOutlineMaterialIcon
#Flags = IsProcessStep

import xml.etree.ElementTree as ET

def __inputs__():
    #CanReference = True
    #Optional = True
    #Description = Production Result, 0 - Unknown, 1 - Pass, 2 - Fail
    Inputs.FailedBoard = new.int(1, 0, 2, 1, 1, "")
    
    #CanReference = True
    #Optional = True
    Inputs.TopBarcode = new.string("")

    #CanReference = True
    #Optional = True
    Inputs.Width = new.double(0, 0, 100000, 1, 10, "mm")

def __run__():
    if Settings.SupervisoryConnection is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    boardAvailableData = Settings.SupervisoryConnection.GetBufferedMessage()

    try:
        boardAvailableTree = ET.fromstring(boardAvailableData)
    except:
        __throwexception__(Exceptions.BadBoardAvailableData)
        return
    
    if Inputs.FailedBoard is not None:
        updateXMLData(boardAvailableTree, "FailedBoard", str(int(Inputs.FailedBoard.Value)))
    
    if Inputs.TopBarcode is not None:
        updateXMLData(boardAvailableTree, "TopBarcode", Inputs.TopBarcode.Value)

    if Inputs.Width is not None:
        updateXMLData(boardAvailableTree, "Width", str(Inputs.Width.Value))
    
    dataToSend = ET.tostring(boardAvailableTree).decode()
    SetBufferedMessage(dataToSend)
    _ReverseTransferStatus_.IsBoardAvailable.Value = True
    if not SendSecondConnection(dataToSend):
        __throwexception__(Exceptions.SendError)
        return

def updateXMLData(xmlMsgTree, attribName, attribValue):
    boardAvailableNode = xmlMsgTree.find("BoardAvailable")
    if boardAvailableNode is not None:
        boardAvailableNode.set(attribName, attribValue)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.ConfigValueRequired = new.exception("#Scripting.Exceptions.ConfigValueRequiredTitle", "#Scripting.Exceptions.ConfigValueRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.SendError = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.SendError", new.enum("Severity", "Error").Value, None)
    Exceptions.BadBoardAvailableData = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.BoardAvailableDataError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    WriteToLog(exception.ExceptionData.FormattedMessage)
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
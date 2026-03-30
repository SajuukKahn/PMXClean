#DisplayName = Parse BoardAvailable Data
#Description = Parse all data from the current BoardAvailable message
#Icon = ClockStartMaterialIcon
#Flags = IsProcessStep, IsTriggerStep

import xml.etree.ElementTree as ET

def __inputs__():
    pass

def __run__():
    boardData = GetBufferedMessage()

    try:
        xmlMsgTree = ET.fromstring(boardData)
    except:
        xmlMsgTree = ""
    
    if xmlMsgTree is not None and xmlMsgTree != "":
        msgNode = xmlMsgTree.find("BoardAvailable")
        if msgNode is not None:
            Outputs.BoardId.Value = str(msgNode.get("BoardId", ""))
            Outputs.BoardIdCreatedBy.Value = str(msgNode.get("BoardIdCreatedBy", ""))
            Outputs.FailedBoard.Value = int(msgNode.get("FailedBoard", "-1"))
            Outputs.ProductTypeId.Value = str(msgNode.get("ProductTypeId", ""))
            Outputs.FlippedBoard.Value = int(msgNode.get("FlippedBoard", "-1"))
            Outputs.TopBarcode.Value = str(msgNode.get("TopBarcode", ""))
            Outputs.BottomBarcode.Value = str(msgNode.get("BottomBarcode", ""))
            Outputs.Length.Value = float(msgNode.get("Length", "-1"))
            Outputs.Width.Value = float(msgNode.get("Width", "-1"))
            Outputs.Thickness.Value = float(msgNode.get("Thickness", "-1"))
            Outputs.ConveyorSpeed.Value = float(msgNode.get("ConveyorSpeed", "-1"))
            Outputs.TopClearanceHeight.Value = float(msgNode.get("TopClearanceHeight", "-1"))
            Outputs.BottomClearanceHeight.Value = float(msgNode.get("BottomClearanceHeight", "-1"))
            Outputs.Weight.Value = float(msgNode.get("Weight", "-1"))
            Outputs.WorkOrderId.Value = str(msgNode.get("WorkOrderId", ""))
            Outputs.BatchId.Value = str(msgNode.get("BatchId", ""))
            Outputs.Route.Value = int(msgNode.get("Route", "-1"))
            Outputs.Action.Value = int(msgNode.get("Action", "-1"))
        else:
            resetOutputs()
    else:
        resetOutputs()


def resetOutputs():
    Outputs.BoardId.Value = ""
    Outputs.BoardIdCreatedBy.Value = ""
    Outputs.FailedBoard.Value = -1
    Outputs.ProductTypeId.Value = ""
    Outputs.FlippedBoard.Value = -1
    Outputs.TopBarcode.Value = ""
    Outputs.BottomBarcode.Value = ""    
    Outputs.Length.Value = -1
    Outputs.Width.Value = -1
    Outputs.Thickness.Value = -1
    Outputs.ConveyorSpeed.Value = -1
    Outputs.TopClearanceHeight.Value = -1
    Outputs.BottomClearanceHeight.Value = -1
    Outputs.Weight.Value = -1
    Outputs.WorkOrderId.Value = ""
    Outputs.BatchId.Value = ""
    Outputs.Route.Value = -1
    Outputs.Action.Value = -1

def __outputs__():
    Outputs.BoardId = new.string("")
    Outputs.BoardIdCreatedBy = new.string("")
    Outputs.FailedBoard = new.int(-1)
    Outputs.ProductTypeId = new.string("")
    Outputs.FlippedBoard = new.int(-1)
    Outputs.TopBarcode = new.string("")
    Outputs.BottomBarcode = new.string("")
    Outputs.Length = new.double(-1, -1, 1000000, 1, 1, "mm")
    Outputs.Width = new.double(-1, -1, 1000000, 1, 1, "mm")
    Outputs.Thickness = new.double(-1, -1, 1000000, 1, 1, "mm")
    Outputs.ConveyorSpeed = new.double(-1, -1, 1000000, 1, 1, "mm/s")
    Outputs.TopClearanceHeight = new.double(-1, -1, 1000000, 1, 1, "mm")
    Outputs.BottomClearanceHeight = new.double(-1, -1, 1000000, 1, 1, "mm")
    Outputs.Weight = new.double(-1, -1, 1000000, 1, 1, "g")
    Outputs.WorkOrderId = new.string("")
    Outputs.BatchId = new.string("")
    Outputs.Route = new.int(-1)
    Outputs.Action = new.int(-1)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
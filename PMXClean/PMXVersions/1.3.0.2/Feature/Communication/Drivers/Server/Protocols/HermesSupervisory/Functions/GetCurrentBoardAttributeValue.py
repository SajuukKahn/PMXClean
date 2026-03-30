#DisplayName = Get Current Board Attribute Value
#Description = Gets value of given attribute
#Icon = NotebookOutlineMaterialIcon
#Flags = IsProcessStep

import xml.etree.ElementTree as ET

def __inputs__():
    Inputs.NodeName = new.string("BoardAvailable")

    Inputs.Attribute = new.enum("HermesBoardAttributes", "BoardId")

def __run__():
    boardData = GetBufferedMessage()

    try:
        xmlMsgTree = ET.fromstring(boardData)
    except:
        Outputs.AttributeValue.Value = ""
        return
    msgNode = xmlMsgTree.find(Inputs.NodeName.Value)
    if msgNode is not None:
        Outputs.AttributeValue.Value = msgNode.get(str(Inputs.Attribute.Value), "")
    else:
        Outputs.AttributeValue.Value = ""

def __outputs__():
    Outputs.AttributeValue = new.string("")

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
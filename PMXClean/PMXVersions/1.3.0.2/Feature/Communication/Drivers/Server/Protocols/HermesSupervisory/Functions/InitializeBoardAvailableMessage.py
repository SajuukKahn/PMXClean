#DisplayName = Initialize BoardAvailable Message
#Description = Initializes BoardAvailable message for the current board if this is the first machine in a Hermes line.
#Icon = TextBoxPlusOutlineMaterialIcon
#Flags = IsProcessStep

import xml.etree.ElementTree as ET

def __inputs__():
    #CanReference = True
    #Description = Production Result, 0 - Unknown, 1 - Pass, 2 - Fail
    Inputs.FailedBoard = new.int(1, 0, 2, 1, 1, "")

    #CanReference = True
    #Description = Board Side Up, 0 - Unknown, 1 - Top, 2 - Bottom
    Inputs.FlippedBoard = new.int(1, 0, 2, 1, 1, "")
    
    #CanReference = True
    #Optional = True
    Inputs.TopBarcode = new.string("")

    #CanReference = True
    #Optional = True
    Inputs.BottomBarcode = new.string("")

    #CanReference = True
    #Optional = True
    Inputs.Width = new.double(0, 0, 100000, 1, 10, "mm")

def __run__():
    if Inputs.FailedBoard is None:
        __throwexception__(Exceptions.InputMissing)
        return

    if Inputs.FlippedBoard is None:
        __throwexception__(Exceptions.InputMissing)
        return
    
    SetBufferedMessage(buildNewMessage())

def buildNewMessage():   
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", GetTimestamp().Timestamp.Value)
    msgChild = ET.SubElement(hermesRoot, "BoardAvailable")
    msgChild.set("BoardId", PVA.System.CreateGUID())
    msgChild.set("BoardIdCreatedBy", Settings.EquipID.Value)
    msgChild.set("FailedBoard", str(int(Inputs.FailedBoard.Value)))
    msgChild.set("FlippedBoard", str(int(Inputs.FlippedBoard.Value)))

    if Inputs.TopBarcode is not None:
        msgChild.set("TopBarcode", Inputs.TopBarcode.Value)
    if Inputs.BottomBarcode is not None:
        msgChild.set("BottomBarcode", Inputs.BottomBarcode.Value)
    if Inputs.Width is not None:
        msgChild.set("Width", str(Inputs.Width.Value))
    
    return ET.tostring(hermesRoot).decode()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.InputMissing = new.exception("#Scripting.Exceptions.ScriptValueRequiredTitle", "#Scripting.Exceptions.ScriptValueRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    WriteToLog(exception.ExceptionData.FormattedMessage)
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
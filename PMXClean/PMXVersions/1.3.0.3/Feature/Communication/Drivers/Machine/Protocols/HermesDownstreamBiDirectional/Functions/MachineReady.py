#DisplayName = Machine Ready (Bi-Directional)
#Description = Signal the adjacent machine that this machine is ready to receive a board.
#Icon = ThumbUpMaterialIcon
#Flags = IsTriggerStep, IsProcessStep

import xml.etree.ElementTree as ET

def __inputs__():
    #CanReference = True
    #Description = Boards Accepted, 0 - Any, 1 - Good, 2 - Failed
    Inputs.FailedBoard = new.int(0, 0, 2, 1, 1, "")

    Inputs.RespondingToBoardForecast = new.bool(False)

    #CanReference = True
    #Optional = True
    Inputs.ForecastID = new.string("")

def __run__():
    if Settings.SupervisoryConnection is None:
        __throwexception__(Exceptions.ConfigValueRequired)
        return

    if Inputs.FailedBoard is None:
        __throwexception__(Exceptions.InputMissing)
        return

    if Inputs.RespondingToBoardForecast is None:
        __throwexception__(Exceptions.InputMissing)
        return

    _ReverseTransferStatus_.IsMachineReady.Value = True

    if Inputs.RespondingToBoardForecast.Value:
        Settings.SupervisoryConnection.SetBufferedMessage(GetBufferedMessage())
    
    if not SendSecondConnection(buildMessage()):
        __throwexception__(Exceptions.SendError)
        return

def buildMessage():
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", Settings.SupervisoryConnection.GetTimestamp().Timestamp.Value)
    msgChild = ET.SubElement(hermesRoot, "MachineReady")
    msgChild.set("FailedBoard", str(int(Inputs.FailedBoard.Value)))
    
    if Inputs.ForecastID is not None:
        msgChild.set("ForecastId", Inputs.ForecastID.Value)
    
    return ET.tostring(hermesRoot).decode()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.SendError = new.exception("#Communication.Exceptions.ErrorTitle", "#Communication.Exceptions.SendError", new.enum("Severity", "Error").Value, None)
    Exceptions.ConfigValueRequired = new.exception("#Scripting.Exceptions.ConfigValueRequiredTitle", "#Scripting.Exceptions.ConfigValueRequired", new.enum("Severity", "Error").Value, None)
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
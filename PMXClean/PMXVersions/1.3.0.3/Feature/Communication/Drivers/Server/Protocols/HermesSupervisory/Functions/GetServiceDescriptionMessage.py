#DisplayName = Get Service Description Message
#Description = Gets ServiceDescription message to send on Hermes connection
#Icon = NotebookOutlineMaterialIcon
#Flags = IsHidden

import xml.etree.ElementTree as ET

def __inputs__():
    pass

def __run__():
    hermesRoot = ET.Element("Hermes")
    hermesRoot.set("Timestamp", GetTimestamp().Timestamp.Value)
    msgChild = ET.SubElement(hermesRoot, "ServiceDescription")
    msgChild.set("MachineId", Settings.EquipID.Value)
    msgChild.set("LaneId", str(int(Settings.LaneID.Value)))
    msgChild.set("Version", "1.6")
    featuresNode = ET.SubElement(msgChild, "SupportedFeatures")
    boardForecastNode = ET.SubElement(featuresNode, "FeatureBoardForecast")
    commandNode = ET.SubElement(featuresNode, "FeatureCommand")
    
    Outputs.Message.Value = ET.tostring(hermesRoot).decode()

def __outputs__():
    Outputs.Message = new.string("")

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
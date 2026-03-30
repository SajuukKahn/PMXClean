#DisplayName = Get Hermes Configuration Data
#Description = Get the Hermes configuration data from the Supervisory connection configuration.
#Icon = DatabaseExportOutlineMaterialIcon
#Flags = IsHidden

def __inputs__():
    pass

def __run__():
    if Settings.EquipID is not None:
        Outputs.EquipID.Value = Settings.EquipID.Value
    
    if Settings.LaneID is not None:
        Outputs.LaneID.Value = Settings.LaneID.Value

    if Settings.CheckAliveFrequency is not None:
        Outputs.CheckAliveFrequency.Value = Settings.CheckAliveFrequency.Value

    if Settings.CheckAliveErrorReporting is not None:
        Outputs.CheckAliveErrorReporting.Value = Settings.CheckAliveErrorReporting.Value

def __outputs__():
    Outputs.EquipID = new.string("")
    Outputs.LaneID = new.int(1, 1, 1000000, 1, 10, "")
    Outputs.CheckAliveFrequency = new.int(1000, 1000, 1000000, 1, 10, "ms")
    Outputs.CheckAliveErrorReporting = new.enum(["Error", "Notification", "Silent"], "Error")

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
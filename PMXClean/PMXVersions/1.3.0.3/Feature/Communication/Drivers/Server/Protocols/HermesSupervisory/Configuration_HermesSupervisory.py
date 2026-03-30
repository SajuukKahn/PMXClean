#AllowedConnectionTypes = EthernetTCP, None
#UsesSecondConnection = False
#ExternalApplicationPath = C:\Program Files\Hermes Test Driver\HermesTestDriver.exe
#EnableLogging = True

def __settings__():
    #DisplayName = Machine ID
    #RetainValue = True
    Settings.EquipID = new.string("")

    #DisplayName = Lane ID
    #RetainValue = True
    Settings.LaneID = new.int(1, 1, 1000000, 1, 10, "")

    #DisplayName = CheckAlive Frequency
    #RetainValue = True
    Settings.CheckAliveFrequency = new.int(1000, 1000, 1000000, 1, 10, "ms")

    #DisplayName = CheckAlive Error Reporting
    #RetainValue = True
    Settings.CheckAliveErrorReporting = new.enum(["Error", "Notification", "Silent"], "Error")

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
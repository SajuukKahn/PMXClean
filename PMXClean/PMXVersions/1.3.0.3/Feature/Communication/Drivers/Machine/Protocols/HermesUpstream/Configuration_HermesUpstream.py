#AllowedConnectionTypes = EthernetTCP
#ExternalApplicationPath = C:\Program Files\Hermes Test Driver\HermesTestDriver.exe
#EnableLogging = True

def __settings__():
    #DisplayName = Supervisory Connection
    #RetainValue = True
    Settings.SupervisoryConnection = new.device("Server", 0)

def onconnect():
    ServiceDescription(new.int(1))

def ondisconnect():
    if IsConnectedToMachine():
        Notification(new.int(5), new.int(4), new.string("Machine Going Offline."))
        PVA.System.Wait(50)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
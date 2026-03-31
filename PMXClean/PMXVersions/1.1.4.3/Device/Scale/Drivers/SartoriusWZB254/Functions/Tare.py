# DisplayName = Tare
# Description = Tare the scale
# Icon = GestureTapMaterialIcon

def __inputs__():
    pass

def __run__():
    SendPacket("T" + Settings.Footer.Value)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
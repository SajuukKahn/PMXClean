# DisplayName = Zero
# Description = Zero the scale
# Icon = Numeric0CircleOutlineMaterialIcon

def __inputs__():
    pass

def __run__():
    SendPacket("V" + Settings.Footer.Value)
    
def __virtual__():
    pass

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
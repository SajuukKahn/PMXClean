#DisplayName = Zero
#Description = Zero the scale
#Icon = Numeric0CircleOutlineMaterialIcon

def __inputs__():
    pass

def __run__():
# Set Terminating character to 0x03
# Zero command has no response 
    SendAndReceive("z" + Settings.Footer.Value, False)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
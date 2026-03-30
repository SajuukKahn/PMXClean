#AllowedConnectionTypes = None
#EnableLogging = False

def __settings__():
    #DisplayName = SMEMA Relationship
    #RetainValue = True
    Settings.MachineRelationship = new.enum("MachineRelationship", "Downstream")

    #DisplayName = Upstream Board Available
    #RetainValue = True
    Settings.UpstreamBoardAvailable = new.input()

    #DisplayName = Upstream Board Available State
    #RetainValue = True
    Settings.UpstreamBoardAvailableState = new.bool(True)
        
    #DisplayName = Upstream Ready
    #RetainValue = True
    Settings.UpstreamReady = new.output()
    
    #DisplayName = Downstream Ready
    #RetainValue = True
    Settings.DownstreamReady = new.input()

    #DisplayName = Downstream Ready State
    #RetainValue = True
    Settings.DownstreamReadyState = new.bool(True)
    
    #DisplayName = Downstream Board Available
    #RetainValue = True
    Settings.DownstreamBoardAvailable = new.output()

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#AllowedConnectionTypes = None

def __settings__():
    #DisplayName = SMEMA Relationship
    Settings.MachineRelationship = new.enum("MachineRelationship", "Downstream")

    #DisplayName = Upstream Board Available
    Settings.UpstreamBoardAvailable = new.input()

    #DisplayName = Upstream Board Available State
    Settings.UpstreamBoardAvailableState = new.bool(True)
        
    #DisplayName = Upstream Ready
    Settings.UpstreamReady = new.output()
    
    #DisplayName = Downstream Ready
    Settings.DownstreamReady = new.input()

    #DisplayName = Downstream Ready State
    Settings.DownstreamReadyState = new.bool(True)
    
    #DisplayName = Downstream Board Available
    Settings.DownstreamBoardAvailable = new.output()

def onconnect():
    pass

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
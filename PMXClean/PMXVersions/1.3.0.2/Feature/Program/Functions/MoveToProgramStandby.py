#DisplayName = Move To Program Standby
#Description = Moves the program's robot to the program's standby position
#Icon = AlphaPBoxMaterialIcon
#SubIcon = MapMarkerMaterialIcon
#Flags = IsProcessStep

def __inputs__():
    #Description = The program whose standby position to move to 
    #CanReference = linked
    Inputs.Program = new.program()

def __run__():
    if Inputs.Program is not None:
        MoveToProgramStandbyByIndex(Inputs.Program.ProgramIndex)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
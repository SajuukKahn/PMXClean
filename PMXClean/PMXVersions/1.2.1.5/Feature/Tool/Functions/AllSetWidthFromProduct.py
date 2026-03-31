#DisplayName = All Set Width From Product
#Description = Move to the width for the current product on all subscribed Tools
#Icon = ValveWidthCustomIcon
#IconIndex = All
#Flags = IsTriggerStep, IsProcessStep, IsProgramStep

def __inputs__():
     #Description = A value indicating whether to execute the PreAdjust triggers
    Inputs.PreAdjust = new.bool(False)

    #Description = A value indicating whether to execute the PostAdjust triggers
    Inputs.PostAdjust = new.bool(False)

def __run__():
    ExecuteGroupAdjust(Inputs.PreAdjust.Value, Inputs.PostAdjust.Value)

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
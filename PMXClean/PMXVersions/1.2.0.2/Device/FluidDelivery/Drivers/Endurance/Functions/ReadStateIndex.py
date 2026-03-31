#DisplayName = Read Unitronics State
#Description = Reads the state of the Unitronics controller
#Icon = BookOpenVariantMaterialIcon

def __inputs__():
    pass

def __run__():
    stateIndexAddress = new.int(20002)
    result = ReadRegister(stateIndexAddress)
    Outputs.Index.Value = result.Result.Value

    if result.Result.Value == 1:
        Outputs.Message.Value = "Ready Mode"
    elif result.Result.Value == 2:
        Outputs.Message.Value = "Manual Mode"
    elif result.Result.Value == 3:
        Outputs.Message.Value = "Setup Mode"
    elif result.Result.Value == 4:
        Outputs.Message.Value = "OEM Mode"
    elif result.Result.Value == 5:
        Outputs.Message.Value = "Fault Mode (System in Error)"
    elif result.Result.Value == 6:
        Outputs.Message.Value = "Cycle Stop / Home Screen"
    elif result.Result.Value == 7:
        Outputs.Message.Value = "Piston / Rod Pump(s) Refilling"
    else:
        Outputs.Message.Value = "INVALID"

def __outputs__():
    #Description = The Endurance Cart state index
    Outputs.Index = new.int(-1)

    #Description = A string representation of the Endurance Cart state
    Outputs.Message = new.string("")

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
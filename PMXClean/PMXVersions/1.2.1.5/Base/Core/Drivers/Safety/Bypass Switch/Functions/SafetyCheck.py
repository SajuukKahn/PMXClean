#DisplayName = Bypass Switch Safety Check
#Description = Perform a safety check on the bypass
#Icon = ShieldCheckMaterialIcon
#Flags = IsHidden

dialogName = "SafetyCheck"

def __inputs__():
    #Description = The maximum amount of time that can pass before the safety check is failed
    Inputs.Timeout = new.int(3000, 0, 1000000, 10, 100, "ms")

def __run__():
    global dialogName
    if (Settings.Input is None):
        PVA.Messaging.SetDialogTitle(dialogName, "#Safety.SafetyCheckFailed")
        PVA.Messaging.SetDialogMessage(dialogName, GetDisplayName() + " #Safety.InputMissing")
        PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
        return

    Outputs.Passed.Value = False
    passedParameter = WaitClosedState(Inputs.Timeout).Passed

    if passedParameter is not None and passedParameter.Value is True:
        Outputs.Passed.Value = True
    else:
        Outputs.Passed.Value = False

def __virtual__():
    pass

def __outputs__():
    #Description = A value indicating the pass/fail status of the safety check
    Outputs.Passed = new.bool(False)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
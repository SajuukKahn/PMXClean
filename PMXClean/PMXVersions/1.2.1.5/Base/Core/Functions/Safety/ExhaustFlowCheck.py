#DisplayName = Exhaust Flow Check
#Description = Perform the initial exhaust flow check
#Icon = FanMaterialIcon
#Flags = IsTriggerStep

dialogName = "ExhaustCheck"

def __inputs__():
    #DisplayName = Exhaust Switch
    #Description = The exhaust switch to check
    Inputs.ExhaustSwitch = new.device("Exhaust Switch", 0)
    
    #DisplayName = Startup Time
    #Description = The warm up time to allow the switch to reach pressure before checks begin
    Inputs.StartupTime = new.int(2000, 0, 1000000, 10, 100, "ms")

    #DisplayName = Check Time
    #Description = The amount of time to perform the exhaust checks over
    Inputs.CheckTime = new.int(60000, 0, 1000000, 10, 100, "ms")

    #DisplayName = Check Interval
    #Description = The amount of time between exhaust checks
    Inputs.CheckInterval = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    global dialogName

    if GetExhaustFlowCheckBypass():
        Outputs.FanError.Value = False
        Outputs.FanPass.Value = False
        return

    if Inputs.ExhaustSwitch is None:
        Outputs.FanError.Value = False
        Outputs.FanPass.Value = False
        __throwexception__(Exceptions.FanInputRequired, "Fan Input")
        return

    if Inputs.ExhaustSwitch.CheckState().Thrown.Value:
        Outputs.FanError.Value = False
        Outputs.FanPass.Value = False
        return

    if GetExhaustCheckPassed():
        return

    exhaustCheckPassed = False

    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogTitle(dialogName, "#Safety.ExhaustCheck")
    PVA.Messaging.SetDialogIcon(dialogName, "FanMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.ExhaustInitialize {:.2f} #Safety.ExhaustUnits #Safety.ExhaustBegin".format(Inputs.StartupTime.Value / 1000))
    PVA.Messaging.SetDialogProgressBarTime(dialogName, int(Inputs.StartupTime.Value))
    PVA.Messaging.ShowDialogAsync(dialogName)

    while not exhaustCheckPassed:
        PVA.Messaging.SetDialogButtonProperties(dialogName, 3, False, False, False, "#Messaging.OK", None)
        PVA.Messaging.SetDialogTitle(dialogName, "#Safety.ExhaustCheck")
        PVA.Messaging.SetDialogIcon(dialogName, "FanMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
        PVA.Messaging.SetDialogMessage(dialogName, "#Safety.ExhaustInitialize {:.2f} #Safety.ExhaustUnits #Safety.ExhaustBegin".format(Inputs.StartupTime.Value / 1000))
        PVA.Messaging.SetDialogProgressBarTime(dialogName, int(Inputs.StartupTime.Value))

        PVA.System.Wait(Inputs.StartupTime.Value)
        PVA.Messaging.SetDialogProgressBarTime(dialogName, 0)

        exhaustCheckPassed = checkExhaust()

    PVA.System.Wait(100)
    PVA.Messaging.SetDialogIcon(dialogName, "CheckBoldMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Green")
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.ExhaustPassed")
    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
    PVA.Messaging.SetDialogTimeout(dialogName, 4000)
    while not PVA.Messaging.CheckDialogInteraction(dialogName):
        PVA.System.Wait(25)

    closeDialog()
    SetExhaustCheckPassed(True)
    StartExhaustFlowMonitor(Inputs)

def __virtual__():
    pass

def checkExhaust():
    global dialogName

    if not Inputs.ExhaustSwitch.CheckState().State.Value:
        Outputs.FanError.Value = True
        Outputs.FanPass.Value = False
        exhaustCheckFailed()
        return False

    timeElapsed = 0
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.ExhaustChecking {:.2f} #Safety.ExhaustUnits".format(Inputs.CheckTime.Value / 1000))
    PVA.Messaging.SetDialogProgressBarTime(dialogName, int(Inputs.CheckTime.Value))

    while (timeElapsed < Inputs.CheckTime.Value and not GetExhaustFlowCheckBypass()):
        PVA.System.Wait(Inputs.CheckInterval.Value)
        timeElapsed += Inputs.CheckInterval.Value
        if not Inputs.ExhaustSwitch.CheckState().State.Value:
            Outputs.FanError.Value = True
            Outputs.FanPass.Value = False
            exhaustCheckFailed()
            return False

        PVA.System.Wait(10)

    return True

def closeDialog():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)

def exhaustCheckFailed():
    global dialogName
    PVA.Messaging.SetDialogProgressBarTime(dialogName, 0)

    PVA.Messaging.SetDialogTitle(dialogName, "#Safety.ExhaustCheckFailed")
    PVA.Messaging.SetDialogIconColor(dialogName, "Red")
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.ExhaustFailed")
    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#Messaging.OK", None)
    PVA.Messaging.SetShutdownButtonIsVisible(dialogName, True)
    PVA.Messaging.SetShutdownButtonIsEnabled(dialogName, True)
    SetExhaustCheckPassed(False)
    while not PVA.Messaging.CheckDialogInteraction(dialogName):
        PVA.System.Wait(25)
    PVA.Messaging.SetShutdownButtonIsVisible(dialogName, False)
    PVA.Messaging.SetShutdownButtonIsEnabled(dialogName, False)

def __outputs__():
    #DisplayName = Fan Error
    #Description = A value indicating whether there was an error with the exhaust check
    Outputs.FanError = new.bool(False)

    #DisplayName = Fan Pass
    #Description = A value indicating whether the exhaust flow check has been completed successfully
    Outputs.FanPass = new.bool(False)

def __exceptions__():
    Exceptions.FanInputRequired = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ExhaustCheckFailure = new.exception("#Safety.Exceptions.ExhaustFailTitle", "#Safety.Exceptions.ExhaustFail", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)

def __exceptionrecovery__():
    pass

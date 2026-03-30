#DisplayName = Wait Broken
#Description = Wait for the curtain to be in the "open" state
#Icon = LightCurtainBrokenCustomIcon
#Flags = IsHidden

dialogName = "SafetyCheck"

def __inputs__():
    #Description = The maximum amount of time to wait for the curtain to reach the desired state
    Inputs.Timeout = new.int(5000, 0, 1000000, 10, 100, "ms")

def __run__():
    global dialogName
    displayName = GetDisplayName()
    referenceName = GetReferenceName()
    PVA.Messaging.CreateDialog(dialogName)

    if (Settings.Input is None):
        PVA.Messaging.SetDialogTitle(dialogName, "#Safety.SafetyCheckFailed")
        PVA.Messaging.SetDialogMessage(dialogName, displayName + " #Safety.InputMissing")
        PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
        while not PVA.Messaging.CheckDialogInteraction(dialogName):
            PVA.System.Wait(25)
        return

    Outputs.Passed.Value = True

    opened = isOpen()
    if opened is False:
        PVA.Messaging.SetDialogTitle(dialogName, "#Messaging.SafetyCheck")
        PVA.Messaging.SetDialogIcon(dialogName, "LightCurtainBrokenCustomIcon")
        PVA.Messaging.SetDialogMessage(dialogName, "#Safety.Break " + displayName)
        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, False)
        PVA.Messaging.SetDialogProgressBarIsDraining(dialogName, True)
        PVA.Messaging.SetDialogProgressBarTime(dialogName, Inputs.Timeout)

        timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
        while (opened is False) and (PVA.System.GetCurrentTime().Value < timeout):
            Outputs.Passed.Value = PVA.Safety.GetAllSafetyDevicesInClosedState(referenceName)
            if Outputs.Passed.Value is False:
                return

            opened = isOpen()
            PVA.System.Wait(10)

        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, False)
        PVA.Messaging.SetDialogProgressBarTime(dialogName, 0)

        if opened is False:
            PVA.Messaging.SetDialogTitle(dialogName, "#Safety.SafetyCheckFailed")
            PVA.Messaging.SetDialogMessage(dialogName,  displayName + " #Safety.BreakFail")
            PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#Messaging.OK", None)
            PVA.Messaging.SetShutdownButtonIsVisible(dialogName, True)
            PVA.Messaging.SetShutdownButtonIsEnabled(dialogName, True)
            while not PVA.Messaging.CheckDialogInteraction(dialogName):
                PVA.System.Wait(25)
            PVA.Messaging.SetDialogButtonProperties(dialogName, 3, False, False, False, "#Messaging.OK", None)
            PVA.Messaging.SetShutdownButtonIsVisible(dialogName, False)
            PVA.Messaging.SetShutdownButtonIsEnabled(dialogName, False)

            Outputs.Passed.Value = False

def __virtual__():
    pass

def isOpen():
    controlPowerOn = PVA.Safety.GetControlPowerOn()
    return (Settings.Input.Value == Settings.StopState.Value) and (controlPowerOn is False)

def __outputs__():
    #Description = A value indicating whether the wait completed successfully or timed out
    Outputs.Passed = new.bool(True, True)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
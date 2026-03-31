#DisplayName = Wait Released
#Description = Wait for the button to be in the "released" state
#Icon = GestureUnTapButtonMaterialIcon
#Flags = IsHidden

dialogName = "SafetyCheck"

def __inputs__():
    #Description = The maximum amount of time to wait for the button to reach the desired state
    Inputs.Timeout = new.int(5000, 0, 1000000, 10, 100, "ms")

def __run__():
    global dialogName
    displayName = GetDisplayName()
    PVA.Messaging.CreateDialog(dialogName)

    if (Settings.Input is None):
        PVA.Messaging.SetDialogTitle(dialogName, "#Safety.SafetyCheckFailed")
        PVA.Messaging.SetDialogMessage(dialogName, displayName + " #Safety.InputMissing")
        PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
        while not PVA.Messaging.CheckDialogInteraction(dialogName):
            PVA.System.Wait(25)
        return

    Outputs.Passed.Value = True

    released = isReleased()
    if released is False:
        PVA.Messaging.SetDialogIcon(dialogName, "GestureUnTapButtonMaterialIcon")
        PVA.Messaging.SetDialogMessage(dialogName, "#Safety.Release " + displayName)

        if (Inputs.Timeout.Value > 0):
            PVA.Messaging.SetDialogProgressBarIsDraining(dialogName, True)
            PVA.Messaging.SetDialogProgressBarTime(dialogName, Inputs.Timeout)

            timeout = PVA.System.GetCurrentTime().Value + Inputs.Timeout.Value
            while (released is False) and (PVA.System.GetCurrentTime().Value < timeout):
                Outputs.Passed.Value = PVA.Safety.GetAllSafetyDevicesInClosedState(displayName)
                if Outputs.Passed.Value is False:
                    return

                released = isReleased()
                PVA.System.Wait(10)

            PVA.Messaging.SetDialogProgressBarTime(dialogName, 0)

        else:
            PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)

            while released is False:
                Outputs.Passed.Value = PVA.Safety.GetAllSafetyDevicesInClosedState(displayName)
                if Outputs.Passed.Value is False:
                    return

                released = isReleased()
                PVA.System.Wait(10)

        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, False)
        PVA.Messaging.SetDialogProgressBarTime(dialogName, 0)

        if released is False:
            PVA.Messaging.SetDialogTitle(dialogName, "#Safety.SafetyCheckFailed")
            PVA.Messaging.SetDialogMessage(dialogName,  displayName + " #Safety.ReleaseFail")
            PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#Messaging.OK", None)
            PVA.Messaging.SetShutdownButtonIsVisible(dialogName, True)
            PVA.Messaging.SetShutdownButtonIsEnabled(dialogName, True)
            while not PVA.Messaging.CheckDialogInteraction(dialogName):
                PVA.System.Wait(25)
            PVA.Messaging.SetDialogButtonProperties(dialogName, 3, False, False, False, "#Messaging.OK", None)
            PVA.Messaging.SetShutdownButtonIsVisible(dialogName, False)
            PVA.Messaging.SetShutdownButtonIsEnabled(dialogName, False)
            PVA.Messaging.SetDialogTitle(dialogName, "#Messaging.SafetyCheck")

            Outputs.Passed.Value = False

def __virtual__():
    pass

def isReleased():
    return (Settings.Input.Value != Settings.StopState.Value)

def __outputs__():
    #Description = A value indicating whether the wait completed successfully or timed out
    Outputs.Passed = new.bool(True)

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
#DisplayName = Control Power On
#Description = Turn the control power output on
#Icon = PowerPlugMaterialIcon
#Flags = IsTriggerStep

dialogName = ""
dialogClosed = False

def __inputs__():
    #DisplayName = Wait Time
    #Description = The amount of time in milliseconds to wait after turning control power on before continuing
    Inputs.WaitTime = new.int(250, 0, 100000, 10, 100, "ms")

    #DisplayName = Show Prompt
    #Description = A value indicating whether the function should prompt the user before turning control power on.
    Inputs.ShowPrompt = new.bool(True)

def __run__():
    global dialogName
    global dialogClosed

    SafetyMonitor()

    if GetControlPowerOn():
        return

    if Inputs.ShowPrompt:
        dialogClosed = False
        dialogName = PVA.Messaging.CreateUniqueDialog()
        PVA.Messaging.SetDialogTitle(dialogName, "#Safety.ControlPower")
        PVA.Messaging.SetDialogIcon(dialogName, "PowerPlugMaterialIcon")
        PVA.Messaging.SetDialogIconColor(dialogName, "Green")
        PVA.Messaging.SetDialogMessage(dialogName, "#Safety.PressOKToContinue")
        PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, False, "#Messaging.OK", dialogMessageChange)
        PVA.Messaging.ShowDialog(dialogName)
        while not dialogClosed:
            PVA.System.Wait(50)
    else:
        SetControlPowerOn()
        PVA.System.Wait(Inputs.WaitTime.Value)

def __virtual__():
    pass

def dialogMessageChange():
    global dialogName
    global dialogClosed
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.RestoreControlPower")
    PVA.Messaging.SetDialogButtonIsVisible(dialogName, 3, False)
    SetControlPowerOn()
    PVA.System.Wait(Inputs.WaitTime.Value)
    PVA.Messaging.CloseDialog(dialogName)
    dialogClosed = True

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    global dialogName
    global dialogClosed
    dialogClosed = True
    PVA.Messaging.CloseDialog(dialogName)

def __exceptionrecovery__():
    pass
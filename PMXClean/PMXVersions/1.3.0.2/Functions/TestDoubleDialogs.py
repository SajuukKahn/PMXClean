#DisplayName = Test Double Dialogs
#Icon = TestTubeMaterialIcon
#IconIndex = 2x
#Flags = IsProcessStep, IsProgramStep, IsTriggerStep

dialog1IsClosed = False
dialog2IsClosed = False

def __inputs__():
    pass

def __run__():
    global dialog1IsClosed
    global dialog2IsClosed

    dialog1IsClosed = False
    dialog2IsClosed = False

    dialog1Name = PVA.Messaging.CreateUniqueDialog()
    dialog2Name = PVA.Messaging.CreateUniqueDialog()

    PVA.Messaging.SetProcessDialog(dialog1Name, 0)
    PVA.Messaging.SetDialogTitle(dialog1Name, "Left Side")
    PVA.Messaging.SetDialogIcon(dialog1Name, "TestTubeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialog1Name, "Green")
    PVA.Messaging.SetDialogMessage(dialog1Name, "Left Side Dialog")
    PVA.Messaging.SetDialogButtonProperties(dialog1Name, 3, True, True, True, "#Messaging.OK", dialog1Closed)

    PVA.Messaging.SetProcessDialog(dialog2Name, 1)
    PVA.Messaging.SetDialogTitle(dialog2Name, "Right Side")
    PVA.Messaging.SetDialogIcon(dialog2Name, "TestTubeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialog2Name, "Blue")
    PVA.Messaging.SetDialogMessage(dialog2Name, "Right Side Dialog")
    PVA.Messaging.SetDialogButtonProperties(dialog2Name, 3, True, True, True, "#Messaging.OK", dialog2Closed)

    PVA.Messaging.ShowProcessDialog(True, "Left - Right Test Dialog")

    while not (dialog1IsClosed and dialog2IsClosed):
        PVA.System.Wait(50)

    PVA.Messaging.CloseProcessDialog(0)
    PVA.Messaging.CloseProcessDialog(1)

    dialog1IsClosed = False
    dialog2IsClosed = False

    dialog1Name = PVA.Messaging.CreateUniqueDialog()
    dialog2Name = PVA.Messaging.CreateUniqueDialog()

    PVA.Messaging.SetProcessDialog(dialog1Name, 0)
    PVA.Messaging.SetDialogTitle(dialog1Name, "Top Side")
    PVA.Messaging.SetDialogIcon(dialog1Name, "TestTubeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialog1Name, "Green")
    PVA.Messaging.SetDialogMessage(dialog1Name, "Top Side Dialog")
    PVA.Messaging.SetDialogButtonProperties(dialog1Name, 3, True, True, True, "#Messaging.OK", dialog1Closed)
    
    PVA.Messaging.SetProcessDialog(dialog2Name, 1)
    PVA.Messaging.SetDialogTitle(dialog2Name, "Bottom Side")
    PVA.Messaging.SetDialogIcon(dialog2Name, "TestTubeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialog2Name, "Blue")
    PVA.Messaging.SetDialogMessage(dialog2Name, "Bottom Side Dialog")
    PVA.Messaging.SetDialogButtonProperties(dialog2Name, 3, True, True, True, "#Messaging.OK", dialog2Closed)

    PVA.Messaging.ShowProcessDialog(False, "Top - Bottom Test Dialog")

    while not (dialog1IsClosed and dialog2IsClosed):
        PVA.System.Wait(50)

    PVA.Messaging.CloseProcessDialog(0)
    PVA.Messaging.CloseProcessDialog(1)

def dialog1Closed():
    global dialog1IsClosed
    dialog1IsClosed = True

def dialog2Closed():
    global dialog2IsClosed
    dialog2IsClosed = True

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
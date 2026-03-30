#DisplayName = Test Tabbed Dialogs
#Icon = TestTubeMaterialIcon
#Flags = IsProcessStep, IsProgramStep, IsTriggerStep

dialog1IsClosed = False
dialog2IsClosed = False
dialog3IsClosed = False

def __inputs__():
    pass

def __run__():
    global dialog1IsClosed
    global dialog2IsClosed
    global dialog3IsClosed

    dialog1IsClosed = False
    dialog2IsClosed = False
    dialog3IsClosed = False

    dialog1Name = PVA.Messaging.CreateUniqueDialog()
    dialog2Name = PVA.Messaging.CreateUniqueDialog()
    dialog3Name = PVA.Messaging.CreateUniqueDialog()

    PVA.Messaging.SetDialogTitle(dialog1Name, "Dialog 1")
    PVA.Messaging.SetDialogIcon(dialog1Name, "TestTubeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialog1Name, "Green")
    PVA.Messaging.SetDialogMessage(dialog1Name, "This is the first test dialog.")
    PVA.Messaging.SetDialogButtonProperties(dialog1Name, 3, True, True, True, "#Messaging.OK", dialog1Closed)

    PVA.Messaging.SetDialogTitle(dialog2Name, "Dialog 2")
    PVA.Messaging.SetDialogIcon(dialog2Name, "TestTubeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialog2Name, "Blue")
    PVA.Messaging.SetDialogMessage(dialog2Name, "This is the second test dialog.")
    PVA.Messaging.SetDialogButtonProperties(dialog2Name, 3, True, True, True, "#Messaging.OK", dialog2Closed)

    PVA.Messaging.SetDialogTitle(dialog3Name, "Dialog 3")
    PVA.Messaging.SetDialogIcon(dialog3Name, "TestTubeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialog3Name, "Red")
    PVA.Messaging.SetDialogMessage(dialog3Name, "This is a high priority test dialog.")
    PVA.Messaging.SetDialogHighPriority(dialog3Name, True)
    PVA.Messaging.SetDialogButtonProperties(dialog3Name, 3, True, True, True, "#Messaging.OK", dialog3Closed)

    PVA.Messaging.ShowDialogAsync(dialog1Name)
    PVA.Messaging.ShowDialogAsync(dialog2Name)
    PVA.Messaging.ShowDialogAsync(dialog3Name)

    while not (dialog1IsClosed and dialog2IsClosed and dialog3IsClosed):
        PVA.System.Wait(50)

def dialog1Closed():
    global dialog1IsClosed
    dialog1IsClosed = True

def dialog2Closed():
    global dialog2IsClosed
    dialog2IsClosed = True

def dialog3Closed():
    global dialog3IsClosed
    dialog3IsClosed = True

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
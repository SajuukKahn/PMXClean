#DisplayName = Test Dialog Input
#Icon = TestTubeMaterialIcon
#IconIndex = In
#Flags = IsProcessStep, IsProgramStep, IsTriggerStep

def __inputs__():
    pass

def __run__():
    test = new.int()
    test2 = new.bool(False)
    test3 = new.string("Replace Me")

    dialogName = PVA.Messaging.CreateUniqueDialog()

    PVA.Messaging.SetDialogTitle(dialogName, "Test Dialog Input")
    PVA.Messaging.SetDialogIcon(dialogName, "TestTubeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Brown")
    PVA.Messaging.SetDialogMessage(dialogName, "Enter Values Below")
    PVA.Messaging.AddDialogUserData(dialogName, "Int", test)
    PVA.Messaging.AddDialogUserData(dialogName, "Bool", test2)
    PVA.Messaging.AddDialogUserData(dialogName, "String", test3)
    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
    PVA.Messaging.ShowDialog(dialogName)

    dialogName = PVA.Messaging.CreateUniqueDialog()

    PVA.Messaging.SetDialogTitle(dialogName, "Dialog Input Results")
    PVA.Messaging.SetDialogIcon(dialogName, "TestTubeMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Green")
    PVA.Messaging.SetDialogMessageWithParameters(dialogName, "Values Entered:\n{0}\n{1}\n{2}", test.Value, test2.Value, test3.Value)
    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
    PVA.Messaging.ShowDialog(dialogName)

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
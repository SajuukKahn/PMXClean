#DisplayName = Safety Check
#Description = Perform the initial safety check to ensure all safety devices are working
#Icon = ShieldCheckMaterialIcon
#Flags = IsTriggerStep

timeout = new.int(5000, 0, 1000000, 10, 100, "ms")
dialogName = "SafetyCheck"

def __inputs__():
    pass

def __run__():
    global dialogName
    PVA.Messaging.CreateDialog(dialogName)

    StopSafetyMonitor()

    devices = buildSafetyDevices()
    inputsGood = checkEachDevicesInput(devices)
    if inputsGood is False:
        return

    PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
    PVA.Messaging.SetDialogTitle(dialogName, "#Messaging.SafetyCheck")
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.Starting")
    PVA.Messaging.ShowDialogAsync(dialogName)

    safetyCheckPassed = False
    while safetyCheckPassed is False:
        allDevicesClosed = False
        while allDevicesClosed is False:
            allDevicesClosed = allDevicesInClosedState(devices)
            PVA.System.Wait(10)

        PVA.Messaging.SetDialogMessage(dialogName, "#Safety.RestoreControlPower")
        controlPowerOn = waitForControlPowerOn()
        if controlPowerOn is True:
            safetyCheckPassed = runSafetyCheck(devices)

        if controlPowerOn is None:
            PVA.Messaging.CloseDialog(dialogName)
            return

        PVA.System.Wait(10)

    SetSafetyCheckComplete(safetyCheckPassed)
    PVA.Messaging.SetDialogIcon(dialogName, "CheckBoldMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Green")
    PVA.Messaging.SetDialogMessage(dialogName, "#Safety.Passed")
    PVA.Messaging.SetDialogTimeout(dialogName, 1000)
    PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
    while not PVA.Messaging.CheckDialogInteraction(dialogName):
        PVA.System.Wait(25)
    PVA.Messaging.CloseDialog(dialogName)
    StartSafetyMonitor()

def __virtual__():
    pass

def buildSafetyDevices():
    devices = []
    for keyValuePair in PVA.Safety:
        if hasattr(keyValuePair.Value, "SafetyCheck"):
            isBypassDevice = IsDoorBypassDevice(keyValuePair)
            isExhaustAndBypassed = IsExhaustDeviceAndBypassed(keyValuePair)
    
            if isBypassDevice is True:
                devices.insert(0, keyValuePair)
            elif isExhaustAndBypassed is False:
                devices.append(keyValuePair)

    return devices

def allDevicesInClosedState(devices):
    global timeout
    global dialogName
    passed = True
    for device in devices:
        passedParameter = device.Value.WaitClosedState(timeout).Passed
        if passedParameter is not None and passedParameter.Value is True:
            passed = passed and passedParameter.Value
        else:
            PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
            passed = False
            break

    return passed

def runSafetyCheck(devices):
    global timeout
    passed = True
    for device in devices:
        passedParameter = device.Value.SafetyCheck(timeout).Passed
        if passedParameter is not None and passedParameter.Value is True:
            passed = passed and passedParameter.Value
        else:
            passed = False
            break

    return passed

def waitForControlPowerOn():
    global timeout
    return  WaitForControlPowerOn(timeout.Value)

def checkEachDevicesInput(devices):
    global dialogName
    for device in devices:
        inputGood = ValidateDeviceInput(device.Key)
        if inputGood is not True:
            PVA.Messaging.SetDialogTitle(dialogName, "#Safety.SafetyCheckFailed")
            PVA.Messaging.SetDialogMessage(dialogName, device.Value.GetDisplayName() + " #Safety.InputMissing")
            PVA.Messaging.SetDialogButtonProperties(dialogName, 3, True, True, True, "#Messaging.OK", None)
            while not PVA.Messaging.CheckDialogInteraction(dialogName):
                PVA.System.Wait(25)
            return False

    return True

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
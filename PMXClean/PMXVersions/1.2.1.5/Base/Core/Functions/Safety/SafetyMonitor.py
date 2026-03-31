#DisplayName = Start Safety Monitor
#Description = Start the machine safety monitor loop to detect changes in safety devices
#Icon = MonitorEyeMaterialIcon
#Flags = IsHidden

timeout = new.int(0)
dialogName = "SafetyCheck"
inProgress = False

def __inputs__():
    pass

def __run__():
    forceClosedState()
    SetSafetyCheckComplete(True)
    StartSafetyMonitor()

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    pass

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)

def __exceptionrecovery__():
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

def forceClosedState():
    global dialogName
    if not GetAllSafetyDevicesInClosedState(""):
        devices = buildSafetyDevices()
        PVA.Messaging.CreateDialog(dialogName)
        PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
        PVA.Messaging.SetDialogTitle(dialogName, "#Messaging.Safety")
        PVA.Messaging.ShowDialogAsync(dialogName)
        allDevicesClosed = False
        while allDevicesClosed is False:
            allDevicesClosed = allDevicesInClosedState(devices)
            PVA.System.Wait(10)
        PVA.Messaging.CloseDialog(dialogName)
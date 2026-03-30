#DisplayName = Clear Boards
#Description = Clear any boards that may exist in the machine to a sensor
#Icon = NotificationClearAllMaterialIcon
#Flags = IsTriggerStep

dialogName = "clearBoard"

def __inputs__():
    #Description = A value indicating whether to reverse the conveyor direction
    Inputs.Reverse = new.bool(False)
    
    #DisplayName = Overall Timeout
    #Description = The maximum amount of time that can pass without any PIP seeing a board
    Inputs.OverallTimeout = new.int(20000, 0, 1000000, 10, 100, "ms")
    
    #DisplayName = PIP Travel Timeout
    #Description = The maximum amount of time that can pass after a board has been detected but has not yet reached the end
    Inputs.PIPTravelTimeout = new.int(4000, 0, 1000000, 10, 100, "ms")
    
    #DisplayName = Stop PIP
    #Description = The PIP sensor the boards are clearing to
    Inputs.StopPIP = new.device("PIP", 2)
    
    #DisplayName = Additional PIPs
    #Description = Any PIP Sensors that should report the existence of a board in the machine
    Inputs.AdditionalPIPs = new.devicelist("PIP", 0, 1)
    
    #DisplayName = Board Stops
    #Description = Any board stops that should be lifted before clearing boards
    Inputs.BoardStops = new.devicelist("Board Stop", 0)

    #Description = Any locators that should be lifted before clearing boards
    Inputs.Locators = new.devicelist("Locator")

def __run__():
    global dialogName

    if Inputs.StopPIP is None:
        __throwexception__(Exceptions.StopPIPNotFound)

    PVA.Messaging.CreateDialog(dialogName)
    PVA.Messaging.SetDialogIcon(dialogName, "NotificationClearAllMaterialIcon")
    PVA.Messaging.SetDialogIconColor(dialogName, "Yellow")
    PVA.Messaging.SetDialogHighPriority(dialogName, True)
    PVA.Messaging.SetDialogTitle(dialogName, "#Staging.ClearBoard")
    PVA.Messaging.SetDialogMessage(dialogName, "#Staging.ClearingBoards " + GetDisplayName() + ". #UI.PleaseWait")
    PVA.Messaging.ShowDialogAsync(dialogName)
    PVA.Messaging.SetDialogProgressBarIsDraining(dialogName, True)
    PVA.Messaging.SetDialogProgressBarTime(dialogName, Inputs.PIPTravelTimeout)

    boardFound = True

    while boardFound:
        boardFound = False
        boardAtEnd = False

        pipTimeoutValue = Inputs.PIPTravelTimeout.Value
        if (pipTimeoutValue > Inputs.OverallTimeout.Value):
            pipTimeoutValue = Inputs.OverallTimeout.Value

        raiseboardstops()
        raiselocators()

        if Inputs.Reverse.Value:
            Reverse()
        else:
            Forward()

        timeout = PVA.System.GetCurrentTime().Value + Inputs.OverallTimeout.Value
        pipTimeout = PVA.System.GetCurrentTime().Value + pipTimeoutValue
        while (PVA.System.GetCurrentTime().Value < pipTimeout) and not (PVA.System.GetCurrentTime().Value > timeout):
            if Inputs.AdditionalPIPs is not None:
                for pip in Inputs.AdditionalPIPs:
                    if pip._PollState_.PolledState.Value and pip._PollState_.IsSettled.Value:
                        PVA.Messaging.SetDialogMessage(dialogName, "#Staging.BoardFound " + Inputs.StopPIP.GetDisplayName() + ". #UI.PleaseWait")   
                        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
                        PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, False)
                        PVA.Messaging.SetDialogProgressBarTime(dialogName, pipTimeout - PVA.System.GetCurrentTime().Value)
                        boardFound = True
                        pipTimeout = PVA.System.GetCurrentTime().Value + pipTimeoutValue

            if Inputs.StopPIP._PollState_.PolledState.Value and Inputs.StopPIP._PollState_.IsSettled.Value:
                boardFound = True
                boardAtEnd = True
                break

            PVA.System.Wait(10)

        Off()

        if boardFound:
            if not boardAtEnd:
                __throwexception__(Exceptions.Timeout)

            PVA.Messaging.SetDialogMessage(dialogName, "#Staging.RemoveBoard")
            PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, True)
            while Inputs.StopPIP._PollState_.PolledState.Value:
                PVA.System.Wait(10)
            PVA.Messaging.SetDialogProgressBarIndeterminate(dialogName, False)
            PVA.Messaging.SetDialogProgressBarIsDraining(dialogName, True)
            PVA.Messaging.SetDialogProgressBarTime(dialogName, Inputs.PIPTravelTimeout.Value)
            PVA.Messaging.SetDialogMessage(dialogName, "#Staging.ClearingBoards " + GetDisplayName() + ". #UI.PleaseWait")

    PVA.Messaging.CloseDialog(dialogName)

def __virtual__():
    pass

def raiseboardstops():
    if (Inputs.BoardStops is not None):
        for boardStop in Inputs.BoardStops:
            boardStop.Up()
        for boardStop in Inputs.BoardStops:
            boardStop.UpCheck(new.int(1000))

def raiselocators():
    if (Inputs.Locators is not None):
        for locator in Inputs.Locators:
            locator.Up()
        for locator in Inputs.Locators:
            locator.UpCheck(new.int(1000))

def __outputs__():
    pass

def __exceptions__():
    Exceptions.Timeout = new.exception("#IO.Exceptions.TimeoutTitle", "#Staging.Exceptions.ClearBoardTimeout", new.enum("Severity", "Error").Value, None)
    Exceptions.StopPIPNotFound = new.exception("#Staging.Exceptions.ClearBoardErrorTitle", "#Staging.Exceptions.ClearBoardError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    global dialogName
    PVA.Messaging.CloseDialog(dialogName)
    ResetSchedule()
    Off()

def __exceptionrecovery__():
    pass
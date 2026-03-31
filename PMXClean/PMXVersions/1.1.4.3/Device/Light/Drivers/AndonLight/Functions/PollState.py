# DisplayName = Poll State
# Description = Poll the states of the andon lights and the alarm and handle blinking/beeping
# Icon = AndonCustomIcon
# Flags = IsPolling, IsHidden

thrown = False
timeout = PVA.System.GetCurrentTime().Value + 2

def __inputs__():
    pass

def __run__():
    global timeout
    try:
        if PVA.System.GetCurrentTime().Value < timeout:
            return
        timeout = PVA.System.GetCurrentTime().Value + Settings.FlashWait.Value
        getStates()
    except:
        return

def __virtual__():
    pass

def getStates():
    global thrown
    red = Settings.RedOutput
    amber = Settings.AmberOutput
    green = Settings.GreenOutput
    alarm = Settings.AlarmOutput

    if red == None or amber == None or green == None or alarm == None:
        if thrown:
            return

        if red == None:
            thrown = True
            __throwexception__(Exceptions.OutputMissing, "Red")
            raise

        if amber == None:
            thrown = True
            __throwexception__(Exceptions.OutputMissing, "Amber")
            raise

        if green == None:
            thrown = True
            __throwexception__(Exceptions.OutputMissing, "Green")
            raise

        if alarm == None:
            thrown = True
            __throwexception__(Exceptions.OutputMissing, "Alarm")
            raise

    thrown = False
    status = GetStatus()

    if status[0] == 1 or (status[0] == 2 and not red.Value):
        Settings.RedOutput.Set(True)
    elif red.Value:
        Settings.RedOutput.Set(False)

    if status[1] == 1 or (status[1] == 2 and not amber.Value):
        Settings.AmberOutput.Set(True)
    elif amber.Value:
        Settings.AmberOutput.Set(False)

    if status[2] == 1 or (status[2] == 2 and not green.Value):
        Settings.GreenOutput.Set(True)
    elif green.Value:
        Settings.GreenOutput.Set(False)

    if status[3] == 1 or (status[3] == 2 and not alarm.Value):
        Settings.AlarmOutput.Set(True)
    elif alarm.Value:
        Settings.AlarmOutput.Set(False)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.OutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.NamedIOMissing", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass

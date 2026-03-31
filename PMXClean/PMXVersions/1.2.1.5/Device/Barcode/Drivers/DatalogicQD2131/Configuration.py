def __settings__():
    Settings.Header = new.string("\x02")
    Settings.Footer = new.string("\x03")
    Settings.Delimiter = new.string(",")
    Settings.NoRead = new.string("NOREAD")

def onconnect():
    # Issue command to read device software version
    softwareVer = SendAndReceive("$+$!", False)
    if softwareVer is None or "QD2131" not in softwareVer:
        raise

    # Beep if enabled (ASCII BEL)
    SendPacket("\x07")

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
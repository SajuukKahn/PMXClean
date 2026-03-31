def __settings__():
    #DisplayName = Air Output
    Settings.AirOutput = new.output()

    #DisplayName = Air Input
    Settings.AirInput = new.input()

def ready():
    pass

def __exceptions__():
    Exceptions.AirOutputMissing = new.exception("#IO.Exceptions.OutputMissingTitle", "#IO.Exceptions.OutputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.AirInputMissing = new.exception("#IO.Exceptions.InputMissingTitle", "#IO.Exceptions.InputMissing", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
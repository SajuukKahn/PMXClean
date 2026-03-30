#DisplayName = Check Error
#Description = Checks for an error and stops execution
#Icon = AlertMaterialIcon
#Flags = IsProcessStep, IsProgramStep, IsTriggerStep, IsInspectionStep
#ThreadSafe = True

def __inputs__():
    #DisplayName = Error State
    #Description = The state that will cause the error to occur.
    #CanReference = True
    Inputs.ErrorState = new.bool(True)

    #Description = The message to show in the error dialog.
    Inputs.Message = new.string("A Problem Has Occurred")

def __run__():
    if Inputs.ErrorState.Value:
        if hasattr(PVA, "Inspection"):
            if PVA.Inspection.IsDesignTime():
                PVA.Notification.ShowNotification(new.enum("NotificationType", "Warning").Value, "#UI.Exceptions.UserDefinedError", Inputs.Message.Value, GetDisplayName(), "", False, False, False)
                return

        __throwexception__(Exceptions.Error)

def __virtual__():
    pass

def __outputs__():
    pass

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([Inputs.Message.Value])
    PVA.Exceptions.ThrowException(exception)

def __exceptions__():
    Exceptions.Error = new.exception("#UI.Exceptions.UserDefinedError", "{0}", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
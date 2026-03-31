#DisplayName = Show Notification
#Description = Show a notification to the user
#Icon = MessageMaterialIcon
#Flags = IsProcessStep, IsProgramStep, IsTriggerStep

def __inputs__():
    #DisplayName = Notification Type
    #Description = The type of notification to show
    Inputs.NotificationType = new.enum("NotificationType", "Information")

    #CanReference = true
    #Description = The header title for this notification
    Inputs.Title = new.string("Title")

    #CanReference = true
    #Description = The message to display in the notification
    Inputs.Message = new.string("Message")

    #DisplayName = Is Persistent
    #Description = A value indicating whether the notification should be persistent
    Inputs.IsPersistent = new.bool(False)

def __run__():
    PVA.Notification.ShowNotification(Inputs.NotificationType.Value, Inputs.Title.Value, Inputs.Message.Value, GetDisplayName(), "", Inputs.IsPersistent.Value, False, False)

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
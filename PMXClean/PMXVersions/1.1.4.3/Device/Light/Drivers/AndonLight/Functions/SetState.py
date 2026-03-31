# DisplayName = Set Andon State
# Description = Set the state of the andon lights and alarm
# Icon = AndonCustomIcon
# Flags = IsProcessStep, IsTriggerStep

def __inputs__():
    #Description = The desired state of the Red andon light
    Inputs.Red = new.enum("OutputState","Off")

    #Description = The desired state of the Amber andon light
    Inputs.Amber = new.enum("OutputState","Off")

    #Description = The desired state of the Green andon light
    Inputs.Green = new.enum("OutputState","Off")

    #Description = The desired state of the alarm
    Inputs.Alarm = new.enum("OutputState","Off")

def __run__():
    states = [int(Inputs.Red.Value), int(Inputs.Amber.Value), int(Inputs.Green.Value), int(Inputs.Alarm.Value)]
    SetStatus(states)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
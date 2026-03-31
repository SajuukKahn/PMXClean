#DisplayName = Single Axis Jog
#Description = Use a discrete or single axis control device to dictate the motion of an axis
#Icon = AxisYArrowLockMaterialIcon
#Flags = IsMappable, IsHidden
#Groups = Motion

def __inputs__():
    #Description = The controller axis to control using the control device
    Inputs.Axis = new.axis("Controller0", 0)
    
    #DisplayName = Axis Inverted
    #Description = A value indicating whether the direction of the control device should be inverted
    Inputs.AxisInverted = new.bool(False)
    
    #DisplayName = Axis Maximum Speed
    #Description = The maximum speed of the controller axis to be controlled by the device
    Inputs.AxisMaxSpeed = new.int(25000, 1, 1000000, 1, 10, "[Unit]/s", Inputs.Axis)
    
    #DisplayName = Axis Acceleration and Deceleration
    #Description = The acceleration and deceleration value of the controller axis to be controlled by the device
    Inputs.AxisAccelDecel = new.int(300000, 1, 10000000, 1, 1000, "[Unit]/s²", Inputs.Axis)
    
    #DisplayName = Slow Factor
    #Description = The factor used to modify the max speed for "slow mode"
    Inputs.SlowFactor = new.double(0.01, 0.0001, 1, 0.001, 0.01, "")

    #Private = True
    #DisplayName = Analog Z
    #Description = The analog value (0 - 1.0) of the device if it is analog
    Inputs.AnalogZ = new.double(0.0, -1.0, 1.0, 0.1, 1.0, "")

def __run__():
    if not Inputs.Axis.IsMotionReady:
        __throwexception__(Exceptions.AxisNotReady)
        return

    analogZ = Inputs.AnalogZ.Value
    if abs(analogZ) < 0.4:
        analogZ = ((analogZ / 0.4) ** 3) * 0.4  # Cubed for greater precision with smaller input

    maxSpeed = abs(int(Inputs.AxisMaxSpeed))

    if IsSlowJog.Value:
        maxSpeed = maxSpeed * Inputs.SlowFactor.Value

    speed = maxSpeed * min(max(analogZ, -1), 1)
    if Inputs.AxisInverted.Value:
        speed = -speed

    jogaxis(Inputs.Axis, speed)

def __virtual__():
    pass

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

    return response

def jogaxis(axis, speed):
    if axis is not None:
        if not axis.IsLocked.Value and not axis.Status[0].Value:
            pos = axis.Position.Value
            if speed < 0:
                limit = axis.ReverseLimit.Value
                speed = max(speed, limit - pos)
            else:
                limit = axis.ForwardLimit.Value
                speed = min(speed, limit - pos)

            sendcommand("JG" + axis.ReferenceName + "=" + str(int(speed)))
            if speed != 0:
                if axis.StopIssued.Value:
                    sendcommand("AC" + axis.ReferenceName + "=" + str(int(Inputs.AxisAccelDecel.Value)))
                    sendcommand("DC" + axis.ReferenceName + "=" + str(int(Inputs.AxisAccelDecel.Value)))
                    sendcommand("BG" + axis.ReferenceName)
                axis.StopIssued.Value = False
            else:
                sendcommand("ST" + axis.ReferenceName)
                WaitMotionComplete([axis])
                axis.StopIssued.Value = True

def __outputs__():
    pass

def __lockresources__():
    if Inputs.Axis is not None:
        Inputs.Axis.Reserve()

def __releaseresources__():
    if Inputs.Axis is not None:
        Inputs.Axis.Release()

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisNotReady = new.exception("#Controller.Exceptions.AxisNotReadyTitle", "#Controller.Exceptions.AxisNotReady", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    if Inputs.Axis is not None:
        StopAxis(Inputs.Axis, True)

def __exceptionrecovery__():
    pass
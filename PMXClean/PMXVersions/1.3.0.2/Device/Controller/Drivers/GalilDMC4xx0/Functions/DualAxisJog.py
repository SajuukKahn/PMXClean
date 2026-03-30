#DisplayName = Dual Axis Jog
#Description = Use a two-axis control device to dictate the motion of two axes
#Icon = AxisXYArrowLockMaterialIcon
#Flags = IsMappable, IsHidden
#Groups = Motion

def __inputs__():
    #DisplayName = Is Coordinated Motion
    #Description = A value indicating whether the axes should be coordinated and allowed to move at the same time
    Inputs.IsCoordinatedMotion = new.bool(True)

    #Optional = True
    #DisplayName = X Axis
    #Description = The controller axis to control using the X axis of the control device
    Inputs.XAxis = new.axis("Controller0", 1)
    
    #DisplayName = X Axis Inverted
    #Description = A value indicating whether the direction of the control device's X Axis should be inverted
    Inputs.XAxisInverted = new.bool(False)
    
    #DisplayName = X Axis Maximum Speed
    #Description = The max speed of the controller axis to be controlled by the X axis
    Inputs.XAxisMaxSpeed = new.int(25000, 1, 1000000, 1, 10, "[Unit]/s", Inputs.XAxis)
    
    #DisplayName = X Axis Acceleration and Deceleration
    #Description = The acceleration and deceleration value of the controller axis to be controlled by the X axis
    Inputs.XAxisAccelDecel = new.int(300000, 1, 10000000, 1, 1000, "[Unit]/s²", Inputs.XAxis)

    #Optional = True
    #DisplayName = Y Axis
    #Description = The controller axis to control using the Y axis of the control device
    Inputs.YAxis = new.axis("Controller0", 0)
    
    #DisplayName = Y Axis Inverted
    #Description = A value indicating whether the direction of the control device's Y Axis should be inverted
    Inputs.YAxisInverted = new.bool(False)
    
    #DisplayName = Y Axis Maximum Speed
    #Description = The max speed of the controller axis to be controlled by the Y axis
    Inputs.YAxisMaxSpeed = new.int(25000, 1, 1000000, 1, 10, "[Unit]/s", Inputs.YAxis)
    
    #DisplayName = Y Axis Acceleration and Deceleration
    #Description = The acceleration and deceleration value of the controller axis to be controlled by the Y axis
    Inputs.YAxisAccelDecel = new.int(300000, 1, 10000000, 1, 1000, "[Unit]/s²", Inputs.YAxis)
    
    #DisplayName = Slow Factor
    #Description = The factor used to modify the max speeds for "slow mode"
    Inputs.SlowFactor = new.double(0.01, 0.0001, 1, 0.001, 0.01, "")

    #Private = True
    #DisplayName = Analog X
    #Description = The analog value (0 - 1.0) of the X axis of the control device
    Inputs.AnalogX = new.double(0.0, -1.0, 1.0, 0.1, 1.0, "")

    #Private = True
    #DisplayName = Analog Y
    #Description = The analog value (0 - 1.0) of the Y axis of the control device
    Inputs.AnalogY = new.double(0.0, -1.0, 1.0, 0.1, 1.0, "")

def __run__():
    analogX = Inputs.AnalogX.Value
    if abs(analogX) < 0.4:
        analogX = ((analogX / 0.4) ** 3) * 0.4  # Cubed for greater precision with smaller input

    analogY = Inputs.AnalogY.Value
    if abs(analogY) < 0.4:
        analogY = ((analogY / 0.4) ** 3) * 0.4  # Cubed for greater precision with smaller input

    maxSpeedX = abs(Inputs.XAxisMaxSpeed.Value)
    maxSpeedY = abs(Inputs.YAxisMaxSpeed.Value)

    if IsSlowJog.Value:
        maxSpeedX = maxSpeedX * Inputs.SlowFactor.Value
        maxSpeedY = maxSpeedY * Inputs.SlowFactor.Value

    speedX = maxSpeedX * min(max(analogX, -1), 1)
    if Inputs.XAxisInverted.Value:
        speedX = -speedX

    speedY = maxSpeedY * min(max(analogY, -1), 1)
    if Inputs.YAxisInverted.Value:
        speedY = -speedY

    if Inputs.IsCoordinatedMotion.Value:
        jogSpeeds = { Inputs.XAxis : int(speedX), Inputs.YAxis : int(speedY) }
    else:
        if abs(analogY) > abs(analogX):
            jogSpeeds = { Inputs.XAxis : 0, Inputs.YAxis : int(speedY) }
        else:
            jogSpeeds = { Inputs.XAxis : int(speedX), Inputs.YAxis : 0 }

    jogaxes(jogSpeeds)

def __virtual__():
    pass

def sendcommand(command):
    response = SendAndReceive(command, False)

    if response is None:
        __throwexception__(Exceptions.NoResponse)
        raise

    return response

def jogaxes(jogSpeeds):
    for axis in jogSpeeds:
        speed = None
        if axis is not None:
            referenceName = axis.GetReferenceName()
            if not axis.IsLocked.Value and not axis.IsInError.Value:
                if not axis.IsMotionReady:
                    __throwexception__(Exceptions.AxisNotReady)
                    return
                pos = axis.Position.Value
                if jogSpeeds[axis] < 0:
                    limit = axis.ReverseLimit.Value
                    speed = max(jogSpeeds[axis], limit - pos)
                else:
                    limit = axis.ForwardLimit.Value
                    speed = min(jogSpeeds[axis], limit - pos)
                sendcommand("JG" + referenceName + "=" + str(int(speed)))
        jogSpeeds[axis] = speed

    for axis in jogSpeeds:
        if axis is not None:
            referenceName = axis.GetReferenceName()
            if axis.Status.Count > 15 and not axis.Status[15]:
                if axis == Inputs.XAxis:
                    sendcommand("AC" + referenceName + "=" + str(int(Inputs.XAxisAccelDecel.Value)))
                    sendcommand("DC" + referenceName + "=" + str(int(Inputs.XAxisAccelDecel.Value)))
                else:
                    sendcommand("AC" + referenceName + "=" + str(int(Inputs.YAxisAccelDecel.Value)))
                    sendcommand("DC" + referenceName + "=" + str(int(Inputs.YAxisAccelDecel.Value)))
                if not axis.IsLocked.Value:
                    sendcommand("BG" + referenceName)

def __outputs__():
    pass

def __lockresources__():
    if Inputs.XAxis is not None:
        Inputs.XAxis.Reserve()
    if Inputs.YAxis is not None:
        Inputs.YAxis.Reserve()

def __releaseresources__():
    if Inputs.XAxis is not None:
        Inputs.XAxis.Release()
    if Inputs.YAxis is not None:
        Inputs.YAxis.Release()

def __exceptions__():
    Exceptions.NoResponse = new.exception("#Connection.Exceptions.NoResponseTitle", "#Connection.Exceptions.NoResponse", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisNotReady = new.exception("#Controller.Exceptions.AxisNotReadyTitle", "#Controller.Exceptions.AxisNotReady", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    StopAxis(Inputs.XAxis, True)
    StopAxis(Inputs.YAxis, True)

def __exceptionrecovery__():
    pass
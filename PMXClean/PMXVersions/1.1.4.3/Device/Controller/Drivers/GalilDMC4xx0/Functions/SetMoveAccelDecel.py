# DisplayName = Set Move Accel Decel
# Description = Set acceleration and deceleration for non-dispense moves
# Icon = RayStartArrowMaterialIcon
# Flags = IsProgramStep, IsHidden
# Groups = Motion

def __inputs__():
    #Private = True
    #Description = The robot to change non-dispense acceleration and deceleration for
    Inputs.Robot = new.robot("Controller0", 0)
    
    #DisplayName = Acceleration
    #Description = The new acceleration value for the non-dispense robot moves
    Inputs.Accel = new.int(300000, 0, 10000000, 1, 10, "[Unit]/s²", Inputs.Robot)
    
    #DisplayName = Deceleration
    #Description = The new deceleration value for the non-dispense robot moves
    Inputs.Decel = new.int(300000, 0, 10000000, 1, 10, "[Unit]/s²", Inputs.Robot)

def __run__():
    robot = Inputs.Robot

    if robot is None:
        PVA.Exceptions.ThrowException(Exceptions.RobotRequired)
        return

    SetMotionVectorAccelDecel(robot, Inputs.Accel.Value, Inputs.Decel.Value)

def __virtual__():
    __run__()

def __outputs__():
    pass

def __exceptions__():
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass
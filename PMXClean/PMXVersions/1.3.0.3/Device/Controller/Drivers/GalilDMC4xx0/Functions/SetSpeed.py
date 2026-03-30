#DisplayName = Set Speed
#Description = Set vector speed on a robot
#Icon = SpeedometerSlowMaterialIcon
#Flags = IsProgramStep, IsHidden
#Groups = Motion

def __inputs__():
    #Private = True
    #Description = The robot to set vector speeds on
    Inputs.Robot = new.robot("Controller0", 0)

    #Description = The speed to set on the robot
    Inputs.Speed = new.int(20000, 2, 1000000, 10, 100, "[Unit]/s", Inputs.Robot)

    #Description = The type (dispense or non-dispense) to change
    Inputs.Type = new.enum("MotionType", "NonDispense")

def __run__():
    robot = Inputs.Robot

    if robot is None:
        PVA.Exceptions.ThrowException(Exceptions.RobotRequired)
        return

    SetVectorSpeed(robot, Inputs.Speed.Value, Inputs.Type)

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
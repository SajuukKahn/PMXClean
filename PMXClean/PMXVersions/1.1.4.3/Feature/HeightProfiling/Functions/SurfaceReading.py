# DisplayName = Surface Reading
# Description = Get the reading of the current surface relative to the substrate
# Icon = HeightMeasureCustomIcon
# Flags = IsHidden

def __inputs__():
    #Private = true
    #Description = The tool to reach the surface with
    Inputs.Tool = new.tool(0)

def __run__():
    profilingtool = Inputs.Tool
    if profilingtool is None:
        __throwexception__(Exceptions.ProfilingToolRequired)
        return

    robot = profilingtool.GetRobot()
    if robot is None:
        __throwexception__(Exceptions.RobotRequired)
        return

    z = robot.ZAxis
    if z is None:
        __throwexception__(Exceptions.AxisRequired, "Z")
        return

    Outputs.Surface.Value = robot.SafeZ.Value

    profilingdevice = GetProfilingDevice(profilingtool)
    if profilingdevice is None:
        __throwexception__(Exceptions.InvalidProfilingDevice)
        return

    if not profilingdevice.IsCalibrated:
        __throwexception__(Exceptions.ProfilingDeviceNotCalibrated)
        return

    if profilingtool.IsOnZAxis():
        # Intentional creation of a new exception - we don't this one to be configurable
        unsupported = new.exception("#HeightProfiling.Exceptions.UnsupportedTitle", "#HeightProfiling.Exceptions.Unsupported", new.enum("Severity", "Error").Value, None)
        __throwexception__(unsupported)
        return

    profileheight = profilingdevice.GetSurfaceReading()
    # will be true when profileheight is NaN
    if profileheight != profileheight:
        __throwexception__(Exceptions.InvalidSurfaceReading)
        return

    Outputs.Surface.Value = profileheight * z.CountsPerMM.Value
    Outputs.Surface.UnitProviderParameter = z.AsParameter()
    Outputs.Surface.IsEnabled = True

def __virtual__():
    pass

def __outputs__():
    #Description = The reading at the current surface relative to the substrate
    Outputs.Surface = new.surface()

def __exceptions__():
    Exceptions.ProfilingToolRequired = new.exception("#HeightProfiling.Exceptions.NoProfileToolTitle", "#HeightProfiling.Exceptions.NoProfileTool", new.enum("Severity", "Error").Value, None)
    Exceptions.RobotRequired = new.exception("#Controller.Exceptions.RobotRequiredTitle", "#Controller.Exceptions.RobotRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)
    Exceptions.ProfilingDeviceNotCalibrated = new.exception("#HeightProfiling.Exceptions.CalibrationErrorTitle", "#HeightProfiling.Exceptions.CalibrationError", new.enum("Severity", "Error").Value, None)
    Exceptions.InvalidProfilingDevice = new.exception("#HeightProfiling.Exceptions.InvalidProfileDeviceTitle", "#HeightProfiling.Exceptions.InvalidProfileDevice", new.enum("Severity", "Error").Value, None)
    Exceptions.InvalidSurfaceReading = new.exception("#HeightProfiling.Exceptions.InvalidSurfaceReadingTitle", "#HeightProfiling.Exceptions.InvalidSurfaceReading", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    Outputs.Surface.Value = 0;
    Outputs.Surface.IsEnabled = False

def __exceptionrecovery__():
    pass
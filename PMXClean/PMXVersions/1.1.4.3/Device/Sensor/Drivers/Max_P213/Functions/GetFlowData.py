# DisplayName = Get Flow Data
# Description = Get a single calibrated flow reading from the sensor and compare it to expected flow
# Flags = IsProgramStep
# Icon = LocationExitMaterialIcon

def __inputs__():
    #DisplayName = Expected Flow
    #Description = The expected flow value at the time of the reading
    Inputs.ExpectedFlow = new.double(0, -2147483647, 2147483646, 0.01, 100, "cc.")
    
    #DisplayName = Clear after Reading
    #Description = A value indicating whether the function should clear the flow data after reading
    Inputs.ClearAfterRead = new.bool(True)
    
    #DisplayName = Error When Out of Deviation
    #Description = A value indicating whether an error should be thrown if the actual flow is outside of the Allowed Deviation
    Inputs.ErrorWhenOutsideDeviation = new.bool(False)
    
    #DisplayName = Allowed Deviation
    #Description = The allowed deviation from the expected flow
    Inputs.AllowedDeviation = new.double(10, 0, 100, 0.1, 100, "%")

def __run__():
    if Settings.Encoder is None:
        __throwexception__(Exceptions.EncoderMissing)
        return

    if Settings.KFactor.Value == 0:
        __throwexception__(Exceptions.KFactorZero)
        return

    Outputs.TargetFlow.Value = Inputs.ExpectedFlow.Value
    Outputs.TargetDeviation.Value = Inputs.AllowedDeviation.Value

    Outputs.Flow.Value = Settings.Encoder.Value / Settings.KFactor.Value
    if Inputs.ExpectedFlow.Value != 0:
        Outputs.Deviation.Value = ((Outputs.Flow.Value - Inputs.ExpectedFlow.Value) / Inputs.ExpectedFlow.Value) * 100.0
    else:
        Outputs.Deviation.Value = float('nan')

    if Inputs.ClearAfterRead.Value:
        ResetFlowData()

    if Inputs.ErrorWhenOutsideDeviation.Value == True:
        if (Outputs.Deviation.Value == float('nan')) or (abs(Outputs.Deviation.Value) > abs(Inputs.AllowedDeviation.Value)):
            Exceptions.DeviationOutOfRange.ExceptionData.MessageParams = tuple([GetDisplayName(), Inputs.AllowedDeviation.Value, Outputs.Deviation.Value, Inputs.ExpectedFlow.Value, Outputs.Flow.Value, Inputs.AllowedDeviation.Units, Inputs.ExpectedFlow.Units])
            PVA.Exceptions.ThrowException(Exceptions.DeviationOutOfRange)
            return

def __virtual__():
    pass

def __outputs__():
    #DisplayName = Target Flow
    #Description = The expected value for the measured flow
    #Property = True
    Outputs.TargetFlow = new.double(0, -2147483647, 2147483646, 0.01, 100, "cc.")
    
    #DisplayName = Actual Flow
    #Description = The actual value of the measured flow
    #Property = True
    Outputs.Flow = new.double(0, -2147483647, 2147483646, 0.01, 100, "cc.")
    
    #DisplayName = Target Deviation
    #Description = The maximum allowed deviation from expected
    #Property = True
    Outputs.TargetDeviation = new.double(0.0, -2147483647, 2147483646, 0.01, 1, "%")
    
    #DisplayName = Actual Deviation
    #Description = The actual deviation from expected
    #Property = True
    Outputs.Deviation = new.double(0.0, -2147483647, 2147483646, 0.01, 1, "%")

def __exceptions__():
    Exceptions.EncoderMissing = new.exception("#IO.Exceptions.EncoderMissingTitle", "#IO.Exceptions.EncoderMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.DeviationOutOfRange = new.exception("#Sensor.DeviationOutOfRange", "{0}\r\n#Sensor.AllowedDeviation: {1:N2}{5}\r\n#Sensor.ActualDeviation: {2:N2}{5}\r\n#Sensor.ExpectedFlow: {3:N2}{6}\r\n#Sensor.ActualFlow: {4:N2}{6}", new.enum("Severity", "Error").Value, None)
    Exceptions.KFactorZero = new.exception("#Sensor.Exceptions.KFactorErrorTitle", "#Sensor.Exceptions.KFactorError", new.enum("Severity", "Silent").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass